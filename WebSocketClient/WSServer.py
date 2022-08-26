from time import sleep
import uuid
import websockets
import asyncio
from google.protobuf import json_format
from proto.game import user_profile_pb2,code_pb2
from proto.gateway import business_pb2

async def echo(websocket,path):
    messagepb = business_pb2.BusinessRequest()
    up = user_profile_pb2.UserProfile(uuid = '111',device_id = '1XXX',push_token = 'token',create_time = 16555555,last_online_time = 15555555,last_offline_time = 155555,level = 1,exp = 0)
    # uip = user_profile_pb2.UserItemPackage(item_package = {101:1})
    code_value = code_pb2.Code.Value('SUCCESS')
    body = user_profile_pb2.UserLoginResponse(code = code_value,user_profile = up,item_package = {101:1},resource_package = {102:1})
    body_byte = body.SerializeToString()
    msg = business_pb2.BusinessResponse(uid = '1111',cmd = 'tmpl.game.UserLoginResponse',body = body_byte)
    msg_byte = msg.SerializeToString()
    print('发送消息：')
    print(body)
    print('*****************')
    async for message in websocket:
        messagepb.ParseFromString(message)
        print('接收消息：')
        print(type(messagepb))
        print(messagepb)
        print('*******************')
        # sleep(5)
        await websocket.send(msg_byte)



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(websockets.serve(echo,'localhost',8765))
    asyncio.get_event_loop().run_forever()