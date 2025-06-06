# comments/views/delete_comment_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comments.models.comment import Comment

class CommentDeleteView(APIView):
    def delete(self, request, project_id, task_number, comment_number):
        user = request.user
        try:
            comment = Comment.objects.get(
                project_id=project_id,
                task_number=task_number,
                comment_number=comment_number,
                user=user,
                deleted=False
            )
        except Comment.DoesNotExist:
            return Response({'error': '삭제 권한이 없거나 댓글이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        comment.deleted = True
        comment.content = "삭제된 댓글입니다"
        comment.save()

        return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_200_OK)
