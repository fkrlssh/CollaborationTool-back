from django.urls import path
from tasks.views.create_task_view import TaskCreateView
from tasks.views.update_task_view import TaskUpdateView
from tasks.views.delete_task_view import TaskDeleteView
from tasks.views.task_detail_view import TaskDetailView
from tasks.views.task_list_view import TaskListView



urlpatterns = [
    path("projects/<int:project_id>/tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("projects/<int:project_id>/tasks/", TaskListView.as_view(), name="task-list"),
    path("projects/<int:project_id>/tasks/<int:task_number>/detail/", TaskDetailView.as_view(), name="task-detail"),
    path("projects/<int:project_id>/tasks/<int:task_number>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("projects/<int:project_id>/tasks/<int:task_number>/delete/", TaskDeleteView.as_view(), name="task-delete"),



]