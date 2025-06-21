from django.urls import path
from projects.views.create_project_view import ProjectCreateView
from projects.views.invite_member_view import InviteMemberView
from projects.views.delete_project_view import ProjectDeleteView
from projects.views.project_list_view import ProjectListView
from projects.views.project_detail_view import ProjectDetailView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:project_id>/invite/', InviteMemberView.as_view(), name='project-invite'),
    path('<int:project_id>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('', ProjectCreateView.as_view(), name='create-project'),
    path('getprojects/', ProjectListView.as_view(), name='project-list'),
    path('<int:project_id>/', ProjectDetailView.as_view(), name='project-detail'),
]
