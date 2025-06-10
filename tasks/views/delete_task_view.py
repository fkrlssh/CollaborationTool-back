# tasks/views/delete_task_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models.task import Task

class TaskDeleteView(APIView):
    def delete(self, request, project_id, task_number):
        try:
            task = Task.objects.get(project_id=project_id, task_number=task_number)
        except Task.DoesNotExist:
            return Response({'error': '해당 업무를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({'message': '업무가 삭제되었습니다.'}, status=status.HTTP_200_OK)
