import os
from django.conf import settings
from files.models.file import File


def delete_file(project_id, task_number, file_number, user=None):
    try:
        file = File.objects.get(
            project_id=project_id,
            task_number=task_number,
            file_number=file_number
        )
    except File.DoesNotExist:
        return False, '파일을 찾을 수 없습니다.'

    if user and file.uploader != user:
        return False, '삭제 권한이 없습니다.'

    abs_path = os.path.join(settings.BASE_DIR, file.file_url.strip('/').replace('/', os.sep))
    if os.path.exists(abs_path):
        os.remove(abs_path)

    file.delete()
    return True, '파일이 삭제되었습니다.'


def delete_all_files(project_id, task_number, user=None):
    files = File.objects.filter(project_id=project_id, task_number=task_number)
    for f in files:
        delete_file(project_id, task_number, f.file_number, user)
