import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):        
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data): 
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            valor_numerico = float(text_data_json.get('message'))
        except ValueError:
            # Si la conversión falla, envía un mensaje de error al cliente
            await self.send(text_data=json.dumps({'error': 'Por favor, envía datos numéricos válidos.'}))
            return  

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))