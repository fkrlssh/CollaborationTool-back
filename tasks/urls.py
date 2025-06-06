from django.urls import path
from tasks.views.create_task_view import TaskCreateView
from tasks.views.update_task_view import TaskUpdateView
from tasks.views.delete_task_view import TaskDeleteView

urlpatterns = [
    path('<int:project_id>/create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:project_id>/<int:task_number>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:project_id>/<int:task_number>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]
