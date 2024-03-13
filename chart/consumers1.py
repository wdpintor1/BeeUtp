import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class ChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["nombre_grupo"]
        self.room_group_name = f"group_{self.group_name}"        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)     
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        try:
            # Procesa los datos del gráfico según tus necesidades
            processed_data = self.process_chart_data(message)
            print(f"Processed Data: {processed_data}")
            if processed_data == -1:
                # Envía un mensaje de error al cliente si process_chart_data devuelve -1
                await self.send(text_data=json.dumps({
                    'message': 'Error en los datos del gráfico'
                }))
            else:
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "chat.message", "message": processed_data}
                )                
               
        except Exception as e:
            # Manejar cualquier otra excepción que pueda ocurrir durante el procesamiento
            await self.send(text_data=json.dumps({
                'message': f'Error durante el procesamiento: {str(e)}'
            }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    def process_chart_data(self, chart_data):
        try:
            valor_numerico = float(chart_data)
            # Lógica de procesamiento aquí
            return valor_numerico
        except ValueError:
            return -1
        except Exception as e:
            print(f"Error en process_chart_data: {e}")
            return -1

