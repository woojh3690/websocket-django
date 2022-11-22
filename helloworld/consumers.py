from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    
  	# websocket 연결 시 실행
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
        self.accept()

	# websocket 연결 종료 시 실행 
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)
        print("close_code : ", close_code)

	# 클라이언트로 부터 수신된 메시지 이벤트 핸들러
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("receive : ", message)

        # 클라이언트로부터 받은 메세지를 다시 클라이언트로 송신
        self.send(text_data=json.dumps({
            'message': "server : " + message
        }))

    # 그룹 메시지 이벤트 핸들러
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': "server : " + event['message']
        }))