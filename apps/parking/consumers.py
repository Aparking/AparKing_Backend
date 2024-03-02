import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class ParkingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        socket_type = text_data_json["type"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": socket_type,
                "message": message
            }
        )

    async def notify_parking_created(self, event):
        await self.send(text_data=event['message'])

    async def notify_parking_booked(self, event):
        await self.send(text_data=event['message'])

    async def notify_parking_deleted(self, event):
        await self.send(text_data=event['message'])

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
