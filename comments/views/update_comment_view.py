# comments/views/update_comment_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comments.models.comment import Comment
from django.utils import timezone

class CommentUpdateView(APIView):
    def put(self, request, project_id, task_number, comment_number):
        user = request.user
        content = request.data.get('content')

        if not content:
            return Response({'error': '수정할 댓글 내용을 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(
                project_id=project_id,
                task_number=task_number,
                comment_number=comment_number,
                user=user,
                deleted=False
            )
        except Comment.DoesNotExist:
            return Response({'error': '수정 권한이 없거나 댓글이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        comment.content = content
        comment.edited = True
        comment.updated_at = timezone.now()
        comment.save()

        return Response({'message': '댓글이 수정되었습니다.'}, status=status.HTTP_200_OK)
