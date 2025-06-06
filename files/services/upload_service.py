# files/services/upload_service.py
import os
from django.conf import settings
from files.models.file import File
from django.utils import timezone

def save_uploaded_file(file, project_id, task_number, uploader):
    # 저장 경로 설정 (Windows 친화적)
    subdir = os.path.join('tasks', f'project_{project_id}', f'task_{task_number}')
    save_path = os.path.join(settings.MEDIA_ROOT, subdir)
    os.makedirs(save_path, exist_ok=True)

    # 실제 파일 저장
    filename = file.name
    full_path = os.path.join(save_path, filename)

    with open(full_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # 파일 URL 생성
    file_url = os.path.join(settings.MEDIA_URL, subdir.replace(os.sep, '/'), filename)

    # 파일 번호 계산
    file_count = File.objects.filter(project_id=project_id, task_number=task_number).count()

    # DB 저장
    File.objects.create(
        project_id=project_id,
        task_number=task_number,
        file_number=file_count + 1,
        uploader=uploader,
        file_name=filename,
        file_url=file_url,
        file_type=file.content_type,
        uploaded_at=timezone.now()
    )

    return file_url
