from django.urls import path
from comments.views.create_comment_view import CommentCreateView
from comments.views.update_comment_view import CommentUpdateView
from comments.views.delete_comment_view import CommentDeleteView


# ✅ 권장: 정식 RESTful 스타일만 사용
urlpatterns = [
    path('projects/<int:project_id>/tasks/<int:task_number>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('projects/<int:project_id>/tasks/<int:task_number>/comments/<int:comment_number>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('projects/<int:project_id>/tasks/<int:task_number>/comments/<int:comment_number>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
