from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CommentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.article = self.scope['url_route']['kwargs']['slug']
        self.article_group_name = 'articles_%s' % self.article
        await self.channel_layer.group_add(
            self.article_group_name,
            self.article
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.article_group_name,
            {
                'type': 'tester_message',
                'tester': 'tester'
            }
        )

    async def tester_message(self, event):
        tester = event['tester']
        await self.send(text_data=json.dumps({
            'tester': tester
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.article_group_name,
            self.article
        )
