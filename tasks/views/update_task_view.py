# tasks/views/update_task_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models.task import Task
from tasks.models.tasklog import TaskLog
from tasks.models.tasktag import TaskTag
from users.models.user import User
from files.services.upload_service import save_uploaded_file
from files.services.delete_service import delete_file
from django.utils import timezone
import ast

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
        tags = request.data.get('tags', [])  # ✅ 태그 리스트

        # 문자열이면 리스트로 파싱 시도
        if isinstance(tags, str):
            try:
                tags = ast.literal_eval(tags)
            except Exception:
                tags = []

        # 담당자 설정
        if assignee_email:
            try:
                assignee = User.objects.get(email=assignee_email)
                if task.assignee != assignee:
                    log_messages.append(f"담당자가 변경됨: {task.assignee} → {assignee}")
                task.assignee = assignee
            except User.DoesNotExist:
                return Response({'error': '담당자 이메일이 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 필드 변경 체크
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

        # DB 업데이트
        Task.objects.filter(project_id=project_id, task_number=task_number).update(
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            assignee=task.assignee,
            updated_at=task.updated_at
        )

        # ✅ 태그 수정: 기존 삭제 후 재생성 (공백 제거 + 중복 제거)
        TaskTag.objects.filter(project_id=project_id, task_number=task_number).delete()

        clean_tags = set()
        for tag in tags:
            if isinstance(tag, str):
                cleaned = tag.strip()
                if cleaned:
                    clean_tags.add(cleaned)

        for tag in clean_tags:
            TaskTag.objects.create(project_id=project_id, task_number=task_number, tag=tag)

        # ✅ 로그 저장
        for msg in log_messages:
            TaskLog.objects.create(
                project=task.project,
                task_number=task.task_number,
                user=user,
                type="update",
                message=msg,
                timestamp=timezone.now()
            )

        # ✅ 파일 삭제
        delete_ids = request.data.get('delete_files', [])
        for file_number in delete_ids:
            delete_file(project_id, task_number, file_number, user)

        # ✅ 파일 업로드
        if 'files' in request.FILES:
            for file in request.FILES.getlist('files'):
                save_uploaded_file(file, project_id, task_number, user)

        return Response({'message': '업무가 수정되었습니다.'}, status=status.HTTP_200_OK)
