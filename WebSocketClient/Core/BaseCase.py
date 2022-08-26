#!/usr/bin/python3
#coding=utf-8
#author: libiqi

from tkinter import E
from turtle import forward
from urllib.request import Request
from websocket import WebSocketConnectionClosedException,WebSocketApp
from google.protobuf import json_format
from proto.kgs.gateway.v1 import client_pb2
from Core.HttpManager import getToken
import json
import _thread
import time
import Logger as log
import random
import string
import importlib
# ws = create_connection('ws://121.40.165.18:8800')
# ws.send('nihao')
# while True:
#     result = ws.recv()
#     if result:
#         print(result)
#     else:
#         break
# print(result)
# ws.close()

def create_string_number(n):
    """生成一串指定位数的字符+数组混合的字符串"""
    m = random.randint(1, n)
    a = "".join([str(random.randint(0, 9)) for _ in range(m)])
    b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
    return ''.join(random.sample(list(a + b), n))

def pb_to_jsonDict(pbStringRequest):
    """将pbstring转化为json格式的dict Response返回"""
    jsonStringRequest=json_format.MessageToDict(pbStringRequest)
    return jsonStringRequest

def jsonDict_to_pb(jsonStringResponse : dict,ProtoBufMessage = client_pb2.RequestForward):
    """将json格式的dict Response转化为pbString返回"""
    pbStringResponse = json_format.ParseDict(jsonStringResponse, ProtoBufMessage())
    return pbStringResponse

def get_path_from_pbMsg(pbPathMsg):
    pbPath = '.'.join(pbPathMsg.split('.')[:-1])
    return pbPath
REGISTER_NAME_LEN = 7 # 随机生成的注册的账号名字长度
REGISTER_PASSWORD = 'a123456' # 注册密码
HTTPURL = ''
# CMD：客户端请求的message路径
CMDPROTOREQ = {
    'game.RequestUserLogin':'proto.game.user_profile_pb2.RequestUserLogin',
    'game.RequestGetShopInfo':'proto.game.user_profile_pb2.RequestGetShopInfo',
    'game.RequestUseItem':'proto.game.user_profile_pb2.RequestUseItem'


}
# CMD：服务器返回的message路径
CMDPROTORSP = {
    'game.ResponseUserLogin':'proto.game.user_profile_pb2.ResponseUserLogin',
    'game.ResponseGetShopInfo':'proto.game.user_profile_pb2.ResponseGetShopInfo',
    'game.NoticeResourceChange':'proto.game.user_profile_pb2.NoticeResourceChange',
    'game.NoticeHeroChange':'proto.game.user_profile_pb2.NoticeHeroChange',
    'game.ResponseUseItem':'proto.game.user_profile_pb2.ResponseUseItem'


}
# 储存请求的CMD和服务器返回的CMD之间的对应关系
REQ_RSP_CMD_MAPPING = {
    'game.RequestUserLogin':'game.ResponseUserLogin',
    'game.RequestGetShopInfo':'game.ResponseGetShopInfo',
    'game.RequestUseItem':'game.ResponseUseItem'
}

class BaseCase():
    def __init__(self,url) -> None:
        self.url = url
        self.correct_cnt = 0
        self.error_cnt = 0
        self.add_check_cnt = 0 # 当前未使用
        self.is_success = True
        self.error_detail =[]
        self.check_dict = {}
        self.msgcnt_checkid = {} # 通过当前第几条消息找check_id 当前未使用
        self.client = WebSocketApp(url,on_message=self.on_message,on_open=self.on_open)
        self.limit_wait_time = 15 # 秒 大于这个时间没收到的消息就算超时，超时的用例response为‘time out’，可能会影响接下来同cmd消息的执行结果
        self.uuid = 'default'
        self.login_msg = {'uuid':self.uuid,'password':REGISTER_PASSWORD}
        self.login_cmd = 'tmpl.game.UserLoginResponse' # 登录的cmd
        self.push_token = '' # 客户端令牌 废弃
        self.token = ''
        self.gateway_login_success = False
        self.login()

    def on_message(self,ws,message):
        messagepb = client_pb2.Response()
        try:
            messagepb.ParseFromString(message)
            msg_dict = pb_to_jsonDict(messagepb)
            # print(msg_dict)
            # print(type(msg_dict))
        except Exception as e:
            log.logError('接收消息格式错误:{1}，ParseFromString失败 错误消息：{0}'.format(message,e))
            return
        if msg_dict.get('login') != None:
            if msg_dict.get('login') == {}:
                self.gateway_login_success = True
            else:
                log.logError('登录gateway失败!!!错误消息：{}'.format(msg_dict))
                ws.close()
        else:
            try:
                cmd = messagepb.forward.cmd
            except Exception as e:
                log.logWarning('接收消息没有cmd 消息内容：{}'.format(messagepb))
                return
            try:
                body = messagepb.forward.body
            except Exception as e:
                log.logWarning('接收消息没有body 消息内容：{}'.format(messagepb))
                return
            if CMDPROTORSP.get(cmd) == None:
                log.logError('接收cmd在表里找不到，请更新 cmd:{}'.format(cmd))
            else:
                pb_path_msg = CMDPROTORSP[cmd]
                pb_path = get_path_from_pbMsg(pb_path_msg)
                pb_msg = pb_path_msg.split('.')[-1]
                try:
                    module = importlib.import_module(pb_path)
                except Exception as e:
                    log.logError(e)
                body_pb = module.__dict__[pb_msg]()
                try:
                    body_pb.ParseFromString(body)
                except Exception as e:
                    log.logError('接收消息中body格式错误:{},ParseFromString失败 错误消息:{}'.format(e,body))
                    return
                body_dict = pb_to_jsonDict(body_pb)
                if cmd == self.login_cmd: # 判断登录返回code是否success，失败则直接报错，不继续后面消息
                    self.push_token = body_dict['userProfile']['pushToken']
                    login_code = body_dict.get('code')
                    if login_code != None and login_code != 0: #code 为0或者None都视为success
                        log.logError('登录失败，错误码：{}'.format(login_code))
                        ws.close()
                for k,v in self.check_dict.items():
                    if REQ_RSP_CMD_MAPPING[v['cmd']] == cmd and v.get('response') == None:
                        self.check_dict[k]['response'] = body_dict
                        print('\n'+cmd+':\n')
                        print(body_dict)
                        break

        return message

    def on_open(self,ws):

        def send_msg():
            need_break = False
            login_msg = self.gateway_login()
            ws.send(login_msg,opcode = 0x2)
            gatewayLogin_start_time = time.time()
            while not self.gateway_login_success:
                cost_time = time.time() - gatewayLogin_start_time
                if  cost_time >= self.limit_wait_time:
                    log.logError('Gateway登录超时')
                    ws.close()
            for k,v in self.check_dict.items():
                current_check_id = k
                current_cmd = v['cmd']
                current_body = v['body']
                current_session = v['session']
                pb_path_msg = CMDPROTOREQ[current_cmd]
                pb_path = get_path_from_pbMsg(pb_path_msg)
                pb_msg = pb_path_msg.split('.')[-1]
                module = importlib.import_module(pb_path)
                current_body_pb = jsonDict_to_pb(current_body,module.__dict__[pb_msg])
                current_body_byte =current_body_pb.SerializeToString()
                msg_dict = {
                    'cmd':current_cmd,
                    'body':current_body_byte,
                    'session':current_session
                }
                # session = client_pb2.Session(uid = msg_dict['session']['uid'],ip = msg_dict['session']['ip'],info = msg_dict['session']['info'])
                msg_pb = client_pb2.RequestForward(cmd = msg_dict['cmd'],body = current_body_byte)
                gateway_msg_pb = client_pb2.Request(forward = msg_pb)
                msg_byte = gateway_msg_pb.SerializeToString()
                try:
                    # print(current_cmd+'\n{}'.format(msg_dict))
                    ws.send(msg_byte,opcode = 0x2)
                except WebSocketConnectionClosedException:
                    log.logError('网络连接已关闭')
                    return
                start_time = time.time()
                while 'response' not in self.check_dict[k]:
                    cost_time = time.time() - start_time
                    if  cost_time >= self.limit_wait_time:
                        if k == 'register' or k == 'login':
                            need_break = True
                            break
                        self.check_dict[k]['response'] = 'time out'
                        log.logWarning('{0} 消息超时！'.format(k))
                if need_break:
                    log.logError('{0}{1}超时！'.format(pb_path_msg,k))
                    break
            ws.close()

        _thread.start_new_thread(send_msg,())

    def do_assert(self,want_value,get_value,check_id):
        if want_value == get_value:
            self.correct_cnt = self.correct_cnt + 1
        else:
            self.error_cnt = self.error_cnt + 1
            self.is_success = False
            self.error_detail.append([check_id,want_value,get_value])

    def add_check(self,check_id,cmd,body):
        """
        按照下面这个格式插入内容，uid是自动加的时间戳 check_dict：
        {
            'check_1':{
                'cmd':cmd,                 'cmd':cmd,          string
                'body':body,               'body':body         bytes
                'session':session          'session':session,  Session                  
            },
            'check_2':{
                'cmd':cmd,                 'cmd':cmd,          string
                'body':body,               'body':body         bytes
                'session':session          'session':session,  Session  
            }
        }

        msgcnt_checkid:
        {'cnt1':check_id,'cnt2':check_id2}
        """
        # uid = int(time.time()*1000000)
        # time.sleep(0.001) # 不等一下运算太快时间戳会重复
        # self.add_check_cnt += 1
        session = {'uid':'1111','ip':'10.96.140.23','info':{'key':'value'}} #TODO
        check_value_dict = {'cmd':cmd,'body':body,'session':session}
        self.check_dict[check_id] = check_value_dict
        # self.msgcnt_checkid[self.add_check_cnt] = check_id

    def get_send(self,check_id):
        return self.check_dict[check_id]['body']

    def get_res(self,check_id):
        try:
            result = self.check_dict[check_id]['response']
        except:
            result = None
        return result

    def run(self):
        pass
        
    def login(self):
        # self.uuid = create_string_number(REGISTER_NAME_LEN)
        # body = {'uuid':self.uuid,'device_id':'','push_token':''}

        body = {'server_id':2}
        self.add_check('login','game.RequestUserLogin',body)

    def gateway_login(self):
        self.token = getToken()
        RequestLogin = client_pb2.RequestLogin()
        RequestLogin.token = self.token
        Requestmsg = client_pb2.Request(login = RequestLogin)
        return Requestmsg.SerializeToString()


if __name__ =='__main__':
    # ws = BaseCase('ws://121.40.165.18:8800')
    # ws.add_check('check_1',19980,'test')
    # ws.client.run_forever()
    # a = json.loads('{"server_id":19980,"req":"test","uid":1651135261952115}')
    # print(a)
    pb_msg = CMDPROTOREQ['login']
    print(get_path_from_pbMsg('pb_msg'))