from rest_framework.views import APIView
from rest_framework.response import Response
from utils.auth import jwt_required

class MeView(APIView):
    @jwt_required
    def get(self, request):
        user = request.user
        return Response({
            "id": user.email,
            "email": user.email,
            "name": user.name,
            # "role": user.role, 
            "lastLogin": user.last_login
        })
