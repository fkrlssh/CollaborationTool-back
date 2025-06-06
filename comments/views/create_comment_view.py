# comments/views/create_comment_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comments.models.comment import Comment
from tasks.models.task import Task
from tasks.models.tasklog import TaskLog
from django.utils import timezone

class CommentCreateView(APIView):
    def post(self, request, project_id, task_number):
        user = request.user
        content = request.data.get('content')

        if not content:
            return Response({'error': '댓글 내용은 비워둘 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(project_id=project_id, task_number=task_number)
        except Task.DoesNotExist:
            return Response({'error': '해당 업무가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        last_comment = Comment.objects.filter(project_id=project_id, task_number=task_number).order_by('-comment_number').first()
        next_comment_number = 1 if not last_comment else last_comment.comment_number + 1

        Comment.objects.create(
            project_id=project_id,
            task_number=task_number,
            comment_number=next_comment_number,
            user=user,
            content=content,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        # ✔ 로그 저장
        TaskLog.objects.create(
            project=task.project,
            task=task,
            user=user,
            type="comment",
            message=f"{user.name}님이 댓글을 작성했습니다.",
            timestamp=timezone.now()
        )

        return Response({'message': '댓글이 작성되었습니다.', 'comment_number': next_comment_number}, status=status.HTTP_201_CREATED)
