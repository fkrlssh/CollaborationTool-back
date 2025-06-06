# tasks/views/update_task_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models.task import Task
from tasks.models.tasklog import TaskLog
from users.models.user import User
from files.services.upload_service import save_uploaded_file
from files.services.delete_service import delete_file
from django.utils import timezone

class TaskUpdateView(APIView):
    def put(self, request, project_id, task_number):
        user = request.user
        try:
            task = Task.objects.get(project_id=project_id, task_number=task_number)
        except Task.DoesNotExist:
            return Response({'error': '해당 업무를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        log_messages = []

        title = request.data.get('title')
        description = request.data.get('description')
        status_value = request.data.get('status')
        due_date = request.data.get('due_date')
        assignee_email = request.data.get('assignee_email')

        if assignee_email:
            try:
                assignee = User.objects.get(email=assignee_email)
                if task.assignee != assignee:
                    log_messages.append(f"담당자가 변경됨: {task.assignee} → {assignee}")
                task.assignee = assignee
            except User.DoesNotExist:
                return Response({'error': '담당자 이메일이 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if title and task.title != title:
            log_messages.append(f"제목 변경: {task.title} → {title}")
            task.title = title
        if description is not None and task.description != description:
            log_messages.append("설명이 변경됨")
            task.description = description
        if status_value and task.status != status_value:
            log_messages.append(f"상태 변경: {task.status} → {status_value}")
            task.status = status_value
        if due_date and str(task.due_date) != due_date:
            log_messages.append(f"마감일 변경: {task.due_date} → {due_date}")
            task.due_date = due_date

        task.updated_at = timezone.now()
        task.save()

        # ✅ 로그 저장
        for msg in log_messages:
            TaskLog.objects.create(
                project=task.project,
                task=task,
                user=user,
                type="update",
                message=msg,
                timestamp=timezone.now()
            )

        # ✅ 파일 삭제 (delete_files = [1, 2, 3])
        delete_ids = request.data.get('delete_files', [])
        for file_number in delete_ids:
            delete_file(project_id, task_number, file_number, user)

        # ✅ 파일 업로드
        if 'files' in request.FILES:
            for file in request.FILES.getlist('files'):
                save_uploaded_file(file, project_id, task_number, user)

        return Response({'message': '업무가 수정되었습니다.'}, status=status.HTTP_200_OK)
