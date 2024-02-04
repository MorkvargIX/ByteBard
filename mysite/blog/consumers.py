import json

from datetime import datetime
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import User, Post, Comment


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_name = self.scope["url_route"]["kwargs"]["post_id"]
        self.post_group_name = f"post_{self.post_name}"

        await self.channel_layer.group_add(self.post_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.post_group_name, self.channel_name)

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        username = text_data_json['username']
        created = datetime.now().isoformat()
        message = text_data_json['message']
        post_id = text_data_json['post_id']

        post = await sync_to_async(Post.objects.get)(pk=post_id)
        user = await sync_to_async(User.objects.get)(username=username)

        comment = await sync_to_async(Comment.objects.create)(post=post, author=user, body=message)

        await self.channel_layer.group_send(self.post_group_name, {
            'type': 'post_message',
            'id': comment.id,
            'username': username,
            'publish': created,
            'message': message
        })

    async def post_message(self, event):
        message = event["message"]
        username = event["username"]
        publish = event["publish"]

        await self.send(text_data=json.dumps({'id': 80, 'username': username, 'publish': publish, 'message': message}))
