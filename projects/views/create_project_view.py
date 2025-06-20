from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.models.project import Project
from projects.models.projectmember import ProjectMember
from users.models.user import User
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProjectCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        name = request.data.get('name')
        description = request.data.get('description', '')
        access = request.data.get('access', False)

        if not name:
            return Response({'error': '프로젝트 이름은 필수입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        project = Project.objects.create(
            name=name,
            description=description,
            owner=user,
            created_at=datetime.now(),
            access=access
        )

        ProjectMember.objects.create(
            project=project,
            user=user,
            role='admin'
        )

        return Response({'message': '프로젝트가 생성되었습니다.', 'project_id': project.id}, status=status.HTTP_201_CREATED)


class ProjectCreateApiView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("name")
        description = data.get("description", "")
        access_raw = data.get("access", 0)
        try:
            access = bool(int(access_raw))
        except (ValueError, TypeError):
            access = False

        owner_email = data.get("ownerId")
        members = data.get("members", [])

        if not name or not owner_email:
            return Response({"error": "name과 ownerId는 필수입니다."}, status=400)

        try:
            owner = User.objects.get(email=owner_email)
        except User.DoesNotExist:
            return Response({"error": "ownerId에 해당하는 사용자가 없습니다."}, status=404)

        with transaction.atomic():
            project = Project.objects.create(
                name=name,
                description=description,
                owner=owner,
                created_at=timezone.now(),
                access=access
            )

            ProjectMember.objects.create(
                project=project,
                user=owner,
                role="admin"
            )

            for m in members:
                email = m.get("email")
                if not email or email == owner.email:
                    continue  

                try:
                    member_user = User.objects.get(email=email)
                    ProjectMember.objects.create(
                        project=project,
                        user=member_user,
                        role=m.get("role", "member")
                    )
                except User.DoesNotExist:
                    continue

        return Response({
            "message": "프로젝트가 생성되었습니다.",
            "project_id": project.id
        }, status=201)
