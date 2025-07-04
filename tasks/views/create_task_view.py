from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from projects.models.project import Project
from tasks.models.task import Task
from tasks.models.tasklog import TaskLog
from tasks.models.tasktag import TaskTag
from files.services.upload_service import save_uploaded_file
from users.models.user import User
from notifications.services.create_notification import create_notification
import json


class TaskCreateView(APIView):
    def post(self, request, project_id):
        user = request.user

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': '해당 프로젝트가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get('title')
        description = request.data.get('description', '')
        assignee_email = request.data.get('assignee_email', '').strip()
        due_date = request.data.get('due_date')
        tags_raw = request.data.get('tags', '[]')

        print("[DEBUG] User 모델:", User)
        print("[DEBUG] assignee_email:", assignee_email)

        try:
            tags = json.loads(tags_raw) if isinstance(tags_raw, str) else tags_raw
        except json.JSONDecodeError:
            tags = []

        if not title or not due_date:
            return Response({'error': '제목과 마감일은 필수입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        assignee_qs = User.objects.filter(email__iexact=assignee_email)
        print("[DEBUG] assignee_qs.exists():", assignee_qs.exists())

        assignee = assignee_qs.first() if assignee_qs.exists() else None

        if assignee_email and not assignee:
            print("[DEBUG] 이메일 매칭된 유저 없음")
            return Response({'error': '담당자 이메일이 유효하지 않습니다.'}, status=400)

        # 업무 번호 정하기
        last_task = Task.objects.filter(project_id=project_id).order_by('-task_number').first()
        next_task_number = 1 if not last_task else last_task.task_number + 1

        # 업무 생성
        task = Task.objects.create(
            project_id=project_id,
            task_number=next_task_number,
            title=title,
            description=description,
            assignee=assignee,
            due_date=due_date,
            status='To Do',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        # 로그
        TaskLog.objects.create(
            task=task,  # ← ForeignKey(Task)
            user=user,
            type="create",
            message=f"업무 '{title}' 생성됨",
            timestamp=timezone.now()
        )

        # 태그
        for tag in tags:
            TaskTag.objects.create(project=project, task_number=next_task_number, tag=tag)

        # 파일
        if 'files' in request.FILES:
            for file in request.FILES.getlist('files'):
                save_uploaded_file(file, project_id, next_task_number, user)

        # 알림
        if assignee:
            create_notification(
                user=assignee,
                type='task_assigned',
                message=f"'{task.title}' 업무가 당신에게 배정되었습니다."
            )

        return Response({'message': '업무가 생성되었습니다.', 'task_number': task.task_number}, status=status.HTTP_201_CREATED)
