from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models.task import Task
from tasks.models.tasklog import TaskLog
from tasks.models.tasktag import TaskTag
from comments.models.comment import Comment
from files.models.file import File
from users.models.user import User
from files.services.delete_service import delete_all_files
from django.utils import timezone


class TaskDeleteView(APIView):
    def delete(self, request, project_id, task_number):
        user = request.user

        try:
            task = Task.objects.get(project_id=project_id, task_number=task_number)
        except Task.DoesNotExist:
            return Response({'error': '해당 업무를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 🔧 오류 원인이었던 부분 수정
        TaskLog.objects.filter(task__project_id=project_id, task__task_number=task_number).delete()

        TaskTag.objects.filter(project_id=project_id, task_number=task_number).delete()
        Comment.objects.filter(project_id=project_id, task_number=task_number).delete()

        delete_all_files(project_id, task_number, user)
        File.objects.filter(project_id=project_id, task_number=task_number).delete()

        task.delete()

        return Response({'message': '업무가 삭제되었습니다.'}, status=status.HTTP_200_OK)
