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

        result = [
            {
                "id": m.project.id,
                "name": m.project.name,
                "description": m.project.description,
                "role": m.role,
                "access": m.project.access,
                "owner": m.project.owner.email,
                "created_at": m.project.created_at,
            }
            for m in memberships
        ]

        return Response(result)
