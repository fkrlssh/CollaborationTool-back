from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from comments.models.comment import Comment
from tasks.models.task import Task
from tasks.models.tasklog import TaskLog
from notifications.services.create_notification import create_notification
from django.utils import timezone

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, task_number):
        user = request.user
        content = request.data.get('content')

        if not content:
            return Response({'error': '댓글 내용은 비워둘 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(project_id=project_id, task_number=task_number)
        except Task.DoesNotExist:
            return Response({'error': '해당 업무가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        last_comment = Comment.objects.filter(project_id=project_id, task_number=task_number)\
                                      .order_by('-comment_number')\
                                      .first()
        next_comment_number = 1 if not last_comment else last_comment.comment_number + 1

        now = timezone.now()
        comment = Comment.objects.create(
            project_id=project_id,
            task_number=task_number,
            comment_number=next_comment_number,
            user=user,
            content=content,
            created_at=now,
            updated_at=now
        )

        TaskLog.objects.create(
            project=task.project,
            task_number=task.task_number,
            user=user,
            type="comment",
            message=f"{user.name}님이 댓글을 작성했습니다.",
            timestamp=now
        )

        if task.assignee and task.assignee != user:
            create_notification(
                user=task.assignee,
                type='comment_posted',
                message=f"{user.name}님이 댓글을 남겼습니다."
            )

        return Response({
            'message': '댓글이 작성되었습니다.',
            'comment': {
                'comment_number': comment.comment_number,
                'user': getattr(user, "name", "익명"),
                'email': user.email,
                'content': comment.content,
                'created_at': str(comment.created_at),  # 문자열로 변환
            }
        }, status=status.HTTP_201_CREATED)

