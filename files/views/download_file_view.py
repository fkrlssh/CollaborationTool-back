# files/views/download_file_view.py
import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from files.models.file import File

class FileDownloadView(APIView):
    def get(self, request, project_id, task_number, file_number):
        try:
            file = File.objects.get(
                project_id=project_id,
                task_number=task_number,
                file_number=file_number
            )
        except File.DoesNotExist:
            raise Http404('파일을 찾을 수 없습니다.')

        abs_path = os.path.join(settings.BASE_DIR, file.file_url.strip('/').replace('/', os.sep))

        if not os.path.exists(abs_path):
            raise Http404('파일이 실제 서버에 존재하지 않습니다.')

        return FileResponse(open(abs_path, 'rb'), as_attachment=True, filename=file.file_name)
