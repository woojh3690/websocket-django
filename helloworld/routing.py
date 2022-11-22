from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from django.core.asgi import get_asgi_application
from . import consumers

# # 백그라운드 메시지 생성
from asgiref.sync import async_to_sync
import threading
import channels
import time

# 클라이언트와 Channels 개발 서버가 연결 될 때, 어느 protocol 타입의 연결인지
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
        ])
    ),
})

# 백그라운드 메시지 생성
def kafkaConsum():  
    time.sleep(3)
    channel_layer = channels.layers.get_channel_layer()

    while True:
        async_to_sync(channel_layer.group_send)(
            "chat",
            {
                'type': 'chat_message',
                'message': "hi"
            }
        )
        time.sleep(2)

t = threading.Thread(target=kafkaConsum)
t.start()
