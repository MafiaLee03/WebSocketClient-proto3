import requests
import json



def getToken(url = 'http://10.96.0.54:12000/entry/login',data = {'token':'ttf001','sdkProvider':''}):
    datajson = json.dumps(data)
    r = requests.post(url,data=datajson)
    return json.loads(r.text)['token']

if __name__ =='__main__':
    url = 'http://10.96.0.54:12000/entry/login'

    data = {'token':'ttf001','sdkProvider':''}
    datajson = json.dumps(data)
    r = requests.post(url,data=datajson)
    print(json.loads(r.text)['token'])