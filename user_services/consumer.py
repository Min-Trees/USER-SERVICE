import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from Friends.models import Request_FriendShip

class FriendRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Khi một WebSocket connection được thiết lập, bạn có thể thực hiện các thao tác tại đây, ví dụ: xác thực người dùng

        # Kết nối vào kênh WebSocket cụ thể dựa trên thông tin người dùng
        self.room_name = f"user_{self.scope['account'].id}"
        self.room_group_name = f"user_{self.scope['account'].id}"

        # Kết nối người dùng vào kênh
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Chấp nhận kết nối WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Ngắt kết nối WebSocket, bạn có thể thực hiện các thao tác dọn dẹp ở đây

        # Ngắt kết nối người dùng khỏi kênh
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_friend_request(self, event):
        # Gửi thông báo realtime đến người dùng
        message = event['message']

        # Gửi thông báo thông qua kết nối WebSocket
        await self.send(text_data=json.dumps({'message': message}))
