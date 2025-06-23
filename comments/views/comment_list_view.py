from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comments.models.comment import Comment


class CommentListView(APIView):
    def get(self, request, project_id, task_number):
        comments = Comment.objects.filter(
            project_id=project_id,
            task_number=task_number,
            deleted=False
        ).order_by('comment_number')

        comment_data = []
        for c in comments:
            comment_data.append({
                'comment_number': c.comment_number,
                'user_email': c.user.email if c.user else None, 
                'content': c.content,
                'edited': bool(c.edited),
                'created_at': c.created_at,
                'updated_at': c.updated_at
            })

        return Response(comment_data, status=status.HTTP_200_OK)
