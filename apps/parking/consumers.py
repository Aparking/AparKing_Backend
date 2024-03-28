import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class ParkingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"{self.room_name}"

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
        message = text_data_json['message']
        socket_type = text_data_json["type"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {'message': message, 'type': socket_type}
        )

    async def notify_parking_created(self, event):
        print("notify_parking_created")
        message_text = json.dumps(event)

        await self.send(text_data=message_text)

    async def notify_parking_booked(self, event):
        print("notify_parking_booked")
        message_text = json.dumps(event)

        await self.send(text_data=message_text)

    async def notify_parking_deleted(self, event):
        print("notify_parking_deleted")
        message_text = json.dumps(event)

        await self.send(text_data=message_text)
