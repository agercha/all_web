import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class DrawConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("doodle", self.channel_name)
        await self.accept()
        
        self.send(json.dumps({
            'type': 'connection_established',
            'message': "You are now connected! Fight on!"
        }))
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        x1 = text_data_json['x1']
        y1 = text_data_json['y1']
        color = text_data_json['color']
        linewidth = text_data_json['linewidth']
        
        await self.channel_layer.group_send(
            "doodle",
            {   
                'type': "draw_message",
                'message': message,
                'x1': x1,
                'y1': y1,
                'color': color,
                'linewidth': linewidth
            }
        )
    
    async def draw_message(self, event):
        message = event['message']
        x1 = event['x1']
        y1 = event['y1']
        color = event['color']
        linewidth = event['linewidth']
        
        await self.send(json.dumps({
            'message': message,
            'x1': x1,
            'y1': y1,
            'color': color,
            'linewidth': linewidth
        }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("doodle", self.channel_name)
        self.close()
         