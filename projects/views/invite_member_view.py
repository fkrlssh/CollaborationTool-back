# projects/views/invite_member_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.models.project import Project
from projects.models.projectmember import ProjectMember
from users.models.user import User
from notifications.services.create_notification import create_notification

class InviteMemberView(APIView):
    def post(self, request, project_id):
        email = request.data.get("email")
        role = request.data.get("role", "member")
        inviter = request.user

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': '프로젝트가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if not ProjectMember.objects.filter(project=project, user=inviter, role='admin').exists():
            return Response({'error': '관리자만 팀원을 초대할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user_to_invite = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': '해당 이메일의 사용자가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if ProjectMember.objects.filter(project=project, user=user_to_invite).exists():
            return Response({'error': '이미 팀원입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        ProjectMember.objects.create(project=project, user=user_to_invite, role=role)

        create_notification(
            user=user_to_invite,
            type='invited',
            message=f"'{project.name}' 프로젝트에 초대되었습니다."
        )
        
        return Response({'message': f'{email} 사용자가 팀원으로 추가되었습니다.'}, status=status.HTTP_200_OK)
