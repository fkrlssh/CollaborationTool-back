from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from projects.models.projectmember import ProjectMember

class ProjectListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        memberships = ProjectMember.objects.select_related('project').filter(user=user)

        result = []

        for m in memberships:
            project = m.project

            # 해당 프로젝트에 속한 모든 멤버 이름과 역할 가져오기
            member_list = ProjectMember.objects.select_related('user').filter(project=project)
            members_data = [
                {
                    "name": member.user.name,
                    "role": member.role
                }
                for member in member_list
            ]

            result.append({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "role": m.role,
                "access": project.access,
                "owner": project.owner.email,
                "created_at": project.created_at,
                "members": members_data
            })

        return Response(result)
