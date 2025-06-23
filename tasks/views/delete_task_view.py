from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models.tasklog import TaskLog
from tasks.models.tasktag import TaskTag
from comments.models.comment import Comment
from files.models.file import File
from files.services.delete_service import delete_all_files

class TaskDeleteView(APIView):
    def delete(self, request, project_id, task_number):
        user = request.user

        # 먼저 존재 여부 확인
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE project_id = %s AND task_number = %s",
                [project_id, task_number]
            )
            count = cursor.fetchone()[0]

        if count == 0:
            return Response({'error': '해당 업무가 존재하지 않습니다.'}, status=404)

        # 연결된 데이터 삭제
        TaskLog.objects.filter(task__project_id=project_id, task__task_number=task_number).delete()
        TaskTag.objects.filter(project_id=project_id, task_number=task_number).delete()
        Comment.objects.filter(project_id=project_id, task_number=task_number).delete()
        delete_all_files(project_id, task_number, user)
        File.objects.filter(project_id=project_id, task_number=task_number).delete()

        # Task 자체 삭제 (Raw SQL)
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE project_id = %s AND task_number = %s",
                [project_id, task_number]
            )

        return Response({'message': '업무가 삭제되었습니다.'}, status=200)
