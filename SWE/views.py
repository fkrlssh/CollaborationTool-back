from django.http import JsonResponse

def test_api(request):
    return JsonResponse({"status": "ok", "message": "ngrok 연결 성공"})