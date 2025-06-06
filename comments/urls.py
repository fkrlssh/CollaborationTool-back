from django.urls import path
from comments.views.create_comment_view import CommentCreateView
from comments.views.update_comment_view import CommentUpdateView
from comments.views.delete_comment_view import CommentDeleteView

urlpatterns = [
    path('<int:project_id>/<int:task_number>/create/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:project_id>/<int:task_number>/<int:comment_number>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('<int:project_id>/<int:task_number>/<int:comment_number>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
