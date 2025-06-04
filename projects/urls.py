from django.urls import path
from projects.views.create_project_view import ProjectCreateView
from projects.views.invite_member_view import InviteMemberView
from projects.views.delete_project_view import ProjectDeleteView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:project_id>/invite/', InviteMemberView.as_view(), name='project-invite'),
    path('<int:project_id>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
]
