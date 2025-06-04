# projects/views/create_project_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.models.project import Project
from projects.models.projectmember import ProjectMember
from users.models.user import User
from datetime import datetime

class ProjectCreateView(APIView):
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
            owner_email=user,
            created_at=datetime.now(),
            access=access
        )

        ProjectMember.objects.create(
            project=project,
            user=user,
            role='admin'
        )

        return Response({'message': '프로젝트가 생성되었습니다.', 'project_id': project.id}, status=status.HTTP_201_CREATED)
