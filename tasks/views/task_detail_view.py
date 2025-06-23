from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tasks.models.task import Task
from tasks.models.tasktag import TaskTag  # ✅ 태그 모델 import
from comments.models.comment import Comment
from files.models.file import File


class TaskDetailView(APIView):
    def get(self, request, project_id, task_number):
        try:
            task = Task.objects.get(project_id=project_id, task_number=task_number)
        except Task.DoesNotExist:
            return Response({'error': '업무를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # ✅ 태그 목록
        tags = list(TaskTag.objects.filter(
            project_id=project_id,
            task_number=task_number
        ).values_list('tag', flat=True))

        # ✅ 첨부파일 목록
        files = File.objects.filter(project_id=project_id, task_number=task_number)
        file_data = [
            {
                'file_number': f.file_number,
                'file_name': f.file_name,
                'file_url': f.file_url
            } for f in files
        ]

        # ✅ 댓글 목록
        comments = Comment.objects.filter(
            project_id=project_id,
            task_number=task_number,
            deleted=False
        ).order_by('comment_number')

        comment_data = [
            {
                'comment_number': c.comment_number,
                'user': c.user.name,
                'content': c.content,
                'edited': c.edited,
                'created_at': c.created_at
            } for c in comments
        ]

        return Response({
            'task_number': task.task_number,
            'title': task.title,
            'description': task.description,
            'assignee': task.assignee.email if task.assignee else None,
            'due_date': task.due_date,
            'status': task.status,
            'tags': tags,               
            'files': file_data,        
            'comments': comment_data   
        }, status=status.HTTP_200_OK)
