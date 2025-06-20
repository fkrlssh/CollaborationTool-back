from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.models.project import Project
from projects.models.projectmember import ProjectMember
from tasks.models.task import Task
from users.models.user import User

class ProjectDetailView(APIView):
    def get(self, request, project_id):
        user = request.user

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': '프로젝트가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 멤버 리스트
        members = ProjectMember.objects.filter(project=project).select_related('user')
        member_data = [
            {
                'email': m.user.email,
                'name': m.user.name,
                'role': m.role
            } for m in members
        ]

        # 업무 리스트
        tasks = Task.objects.filter(project_id=project.id).order_by('task_number')
        task_data = [
            {
                'task_number': t.task_number,
                'title': t.title,
                'status': t.status,
                'due_date': t.due_date
            } for t in tasks
        ]

        return Response({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at,
            'members': member_data,
            'tasks': task_data
        }, status=status.HTTP_200_OK)
