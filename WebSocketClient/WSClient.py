from tracemalloc import start
from urllib import response
from locust import User,task,events,constant
import time
from requests import request
import websocket
import ssl
import json
import jsonpath

def eventType_success(eventType,recvText,total_time):
    events.request_success.fire(request_type = "[RECV]",
                                name = eventType,
                                response_time = total_time,
                                response_length = len(recvText))

class WebSocketClient(object):

    _locust_environment = None

    def __init__(self,host) -> None:
        self.host = host
        self.ws = websocket.WebSocket(sslopt = {"cert_reqs": ssl.CERT_NONE}) #关掉ssl校验

    def connect(self,burl):
        start_time = time.time()
        try:
            self.conn = self.ws.connect(url = burl)
        except websocket.WebSocketConnectionClosedException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type = "[Connect]",name = 'Connection is already closed',response_time = total_time,exception = e)
        except websocket.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type = "[Connect]",name = 'Timeout',response_time = total_time,exception = e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type = "[Connect]",name = 'WebSocket',response_time = total_time,response_length = 0)
        return self.conn

    def recv(self):
        return self.ws.recv()

    def send(self,msg):
        self.ws.send(msg)

class WebSocketUser(User):
    
    abstract = True

    def __init__(self,*args,**kw):
        super(WebSocketUser,self).__init__(*args,**kw)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment

class ApiUser(WebSocketUser):
    host = "ws://121.40.165.18:8800"
    wait_time = constant(0)
    @task(1)
    def pft(self):
        self.url = "ws://121.40.165.18:8800" # wss地址
        self.data = {}
        self.client.connect(self.url)
        
        sendMsg = '1'
        self.client.send(sendMsg)

        while True:
            # 消息接收计时
            start_time = time.time()
            recv = self.client.recv()
            total_time = int((time.time() - start_time)*1000)

            try:
                recv_dict = json.loads(recv)
                eventType_s = jsonpath.jsonpath(recv_dict,expr='$.eventType')
                eventType_success(eventType_s[0],recv,total_time)
            except websocket.WebSocketConnectionClosedException as e:
                events.request_failure.fire(request_type = "[ERROR] WebSocketConnectionClosedException",name = 'Connection is already closed.',response_time = total_time,exception = e)
            except:
                print(recv)
                if 'ok' in recv:
                    eventType_success('ok','ok',total_time)

if __name__ == '__main__':
    pass