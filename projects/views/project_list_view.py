from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.models.project import Project
from projects.models.projectmember import ProjectMember
from tasks.models.task import Task

class ProjectListView(APIView):
    def get(self, request):
        user = request.user

        # 내가 속한 프로젝트들
        memberships = ProjectMember.objects.filter(user=user).select_related('project')
        data = []

        for membership in memberships:
            project = membership.project

            # 각 프로젝트의 업무 목록(title만)
            tasks = Task.objects.filter(project_id=project.id).values('task_number', 'title')

            data.append({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "my_role": membership.role,
                "tasks": list(tasks)
            })

        return Response(data, status=status.HTTP_200_OK)
