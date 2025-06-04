from django.http import JsonResponse

def test_api(request):
    return JsonResponse({"status": "ok", "message": "서버 연결 성공"})