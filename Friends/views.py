from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from User.models import Account
from rest_framework import generics, status
from http import HTTPStatus
from .models import Request_FriendShip, FriendShip
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.response import Response 
###################################################
## đề xuất kết bạn
class Friends_Request(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(Account, id = user_id)
        similar_users = self.calculate_similarity(user)
        list_request = [user.id for user in similar_users]
        return JsonResponse({"list_request_id": list_request})
    # ham tim su giong nhau
    def calculate_similarity(self, user):
        similar_users = Account.objects.filter(
            department=user.department,
            classroom=user.classroom
        ).exclude(id=user.id)

        return similar_users
    
class SendFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from_user = request.user
        to_user = request.data.get('to_user')
        status_request = request.data.get('status')

        try:
            # Kiểm tra xem yêu cầu kết bạn đã tồn tại hay chưa
            existing_request = Request_FriendShip.objects.get(from_user=from_user, to_user=to_user, status=status_request)
            response_data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'service_name': 'FRIENDSHIPSERVICE',
                'body': {
                    'data': 'NULL',
                    'error': 'Request already exists'
                }
            }
            return Response(response_data, status=response_data['status'])
        except Request_FriendShip.DoesNotExist:
            # Tạo yêu cầu kết bạn mới
            friend_request = Request_FriendShip(from_user=from_user, to_user=to_user, status=status_request)
            friend_request.save()

            # Gửi thông báo realtime (nếu đã cấu hình Django Channels)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_{to_user}",  # Thay user_id bằng ID của người nhận
                {
                    'type': 'send.friend.request',
                    'message': 'You have a new friend request.'
                }
            )
            # Thêm mã xử lý thông báo realtime ở đây

            response_data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Created',
                'service_name': 'FRIENDSHIPSERVICE',
                'body': {
                    'data': {
                        'message': 'Send friend request successfully',
                        'from_user': friend_request.from_user,
                        'to_user': friend_request.to_user,
                        'status': friend_request.status
                    }
                }
            }
            return Response(response_data, status=response_data['status'])

def list_friends(request, user_id):
    friends = FriendShip.objects.filter(status = 'ACCEPTED', )