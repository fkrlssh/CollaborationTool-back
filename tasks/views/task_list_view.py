# tasks/views/task_list_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models.task import Task
from projects.models.project import Project

class TaskListView(APIView):
    def get(self, request, project_id):
        # 프로젝트 존재 여부 확인
        try:
            Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "해당 프로젝트가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 해당 프로젝트의 업무 조회
        tasks = Task.objects.filter(project_id=project_id).order_by("task_number")

        # 리스트 반환
        task_list = [
            {
                "task_number": task.task_number,
                "title": task.title,
                "status": task.status,
                "due_date": task.due_date,
                "assignee": task.assignee.email if task.assignee else None,
                "description": task.description,
            }
            for task in tasks
        ]

        return Response({"tasks": task_list}, status=status.HTTP_200_OK)
