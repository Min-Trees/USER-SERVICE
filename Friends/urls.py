from django.urls import path
from .views import SendFriendRequest, Friends_Request

urlpatterns = [
    path('friends/<str:user_id>/', SendFriendRequest.as_view(), name='SendFriendRequest'),
    path('friend-request/', Friends_Request.as_view(), name='friend_request'),
]
