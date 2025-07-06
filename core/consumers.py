import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import TaskResult

class TaskProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = f'task_{self.task_id}'

        # Join task group
        await self.channel_layer.group_add(
            self.task_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave task group
        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Send current task status
        task_status = await self.get_task_status()
        await self.send(text_data=json.dumps(task_status))

    async def task_update(self, event):
        # Send task update to WebSocket
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def get_task_status(self):
        try:
            task = TaskResult.objects.get(task_id=self.task_id)
            return {
                'task_id': task.task_id,
                'status': task.status,
                'progress': task.progress,
                'error': task.error
            }
        except TaskResult.DoesNotExist:
            return {'error': 'Task not found'}
