# comments/views/delete_comment_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from comments.models.comment import Comment


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ DRF 인증 방식 적용

    def delete(self, request, project_id, task_number, comment_number):
        user = request.user

        # 댓글 찾기: 해당 user가 쓴 댓글 중 삭제되지 않은 것
        comment = Comment.objects.filter(
            project_id=project_id,
            task_number=task_number,
            comment_number=comment_number,
            user=user,
            deleted=False
        ).first()

        if not comment:
            return Response(
                {'error': '삭제 권한이 없거나 댓글이 존재하지 않습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ save() 대신 update() 사용 (복합키 구조 대응)
        Comment.objects.filter(
            project_id=project_id,
            task_number=task_number,
            comment_number=comment_number,
            user=user
        ).update(
            deleted=True,
            content="삭제된 댓글입니다."
        )

        return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_200_OK)
