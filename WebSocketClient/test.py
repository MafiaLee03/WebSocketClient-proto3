from google.protobuf import json_format
import json
from proto.gateway import business_pb2
def pb_to_json(pbStringRequest):
    """将pbstring转化为jsonStringResponse返回"""
    jsonStringRequest=json_format.MessageToJson(pbStringRequest)
    return jsonStringRequest

def json_to_pb(jsonStringResponse):
    """将jsonStringResponse转化为pbString返回"""
    pbStringResponse = json_format.Parse(json.dumps(jsonStringResponse))
    return pbStringResponse
def get_path_from_pbMsg(pbMsg):
    pbPath = '.'.join(pbMsg.split('.')[:-2])
    return pbPath
CMDPROTO = {
    'login':'protobuf.game.user_pb2.UserLoginReq'


}
class A():
    class b():
        pass
if __name__ == '__main__':
    # json_obj={'name':'fcao','value':'0.74','descibe':'202102241339'}
    # request=json_to_pb(json_obj)
    # print(request)
    # print(type(request))
    # json_result = pb_to_json(request)
    # print(json_result)
    # print(type(json_result))
    # pb_msg = CMDPROTO['login']
    # print(get_path_from_pbMsg(pb_msg))
    # print(pb_msg.split('.')[-1])
    print(type(business_pb2.BusinessRequest))