# -*- coding: utf-8 -*-#
# file:         socketio
# Author:       ShunZhe
# Date:         2021/6/26


import json
import logging
import re
import time

import gevent
import websocket
from locust import User,task

"""自定义websocket客户端"""

header = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36 '

}

class SocketIO(object):
    _locust_environment = None
    start_time = 0

    def __init__(self):
        self.events = None
        self.ws = None

    def _require_failure(self, name, response_time, message, action, context, **kwargs):
        """统计失败请求数"""
        self.events.request_failure.fire(
            request_type="接收数据",
            name=name,
            response_time=response_time,
            response_length=len(message),
            exception=f'{action} Content Error!',
            context=context,
        )

    def _require_success(self, name, response_time, message, **kwargs):
        """统计成功请求数"""
        self.events.request_success.fire(
            request_type="接收数据",
            name=name,
            response_time=response_time,
            response_length=len(message),
        )

    def _require_fire(self, name, response_time, message, context, **kwargs):
        """通用统计请求数"""
        self.events.request.fire(
            request_type="接收数据",
            name=name,
            response_time=response_time,
            response_length=len(message),
            exception=None,
            context=context,
        )

    def connect(self, host):
        """建立连接"""
        self.ws = websocket.create_connection(host, header=header)
        gevent.spawn(self.receive)

    def receive(self, context=None):
        """接收事件下发数据"""
        message_regex = re.compile(r"(\d*)(.*)")
        while True:
            message = self.ws.recv()
            total_time = int((time.time() - self.start_time) * 1000)  # 统计响应时间
            logging.info(f"WSR: {message}")
            m = message_regex.match(message)
            if m is None:
                raise Exception(f"got no matches in {message}")
            code = m.group(1)  # 正则获取code
            json_string = m.group(2)  # 正则获取下发数据
            if code == "0":
                name = "0 open"
            elif code == "3":
                name = "3 heartbeat"
            elif code == "40":
                name = "40 message ok"
            elif code == "42":
                """
                根据具体的业务场景统计请求的成功或者失败情况
                此处校验op操作如果length返回小于1则为失败
                """
                obj = json.loads(json_string)
                ts_type, payload = obj
                name = f"{code} {ts_type}"
                if 'operation_ack' == ts_type:
                    """定义op操作成功、失败断言"""
                    if payload['code'] == 1 and payload['length'] >= 1:
                        self._require_success(name, total_time, message)
                    else:
                        self._require_failure(name, total_time, message, ts_type, context)

                elif 'set_doc_ack' == ts_type:
                    """定义set_doc操作成功、失败断言"""
                    if payload['code'] == 1:
                        self._require_success(name, total_time, message)
                    else:
                        self._require_failure(name, total_time, message, ts_type, context)

            else:
                logging.info(f"Received unexpected message: {message}")
                continue
            if name in ('42 operation_ack', '42 set_doc_ack'):
                pass
            else:
                self._require_fire(name, total_time, message, context)

    def send(self, body, context=None):
        """发送数据"""
        if context is None:
            context = {}
        if body == "2":
            action = "2 heartbeat"
        else:
            m = re.compile(r"(\d*)(.*)").match(body)
            assert m is not None
            code = m.group(1)
            action = m.group(2).split(',')[0].split('\"')[1]
            action = f"{code} {action}"
        self._require_fire(name=action, response_time=None, message=body, context=context)
        logging.info(f"WSS: {body}")
        self.start_time = time.time()  # 开始发送数据的时间
        self.ws.send(body)

    def sleep_with_heartbeat(self, seconds):
        """模拟心跳"""
        while seconds >= 0:
            gevent.sleep(min(15, seconds))
            seconds -= 15
            self.send("2")
            # logging.info('模拟心跳～')


class SocketIOUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(SocketIOUser, self).__init__(*args, **kwargs)
        self.client = SocketIO()
        self.client._locust_environment = self.environment
        self.client.events = self.environment.events

class MyUser(SocketIOUser):

    @task(1)
    def pft(self):
        self.url = "ws://localhost:8765/" # wss地址
        self.data = {}
        self.client.connect(self.url)
        
        sendMsg = '1'
        self.client.send(sendMsg)