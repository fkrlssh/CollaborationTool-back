# projects/views/delete_project_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.models.project import Project
from projects.models.projectmember import ProjectMember

class ProjectDeleteView(APIView):
    def delete(self, request, project_id):
        user = request.user
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': '프로젝트가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if not ProjectMember.objects.filter(project=project, user=user, role='admin').exists():
            return Response({'error': '관리자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response({'message': '프로젝트가 삭제되었습니다.'}, status=status.HTTP_200_OK)
