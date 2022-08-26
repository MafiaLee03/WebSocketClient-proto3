import json
import requests

def log(data):
    print(data)

def logError(st):
    print('\033[1;31m {0} \033[0m'.format(st))

def logWarning(st):
    print('\033[1;33m {0} \033[0m'.format(st))

def flyBook(message):
    url = 'https://open.feishu.cn/open-apis/bot/v2/hook/68c79855-f43e-4584-b64a-3b79c62de9f8'
    payload_message = {
    "msg_type": "text",
    "content": {
        "text": message
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=json.dumps(payload_message))

def fbSend(j,jenkins_url = None):
    url = 'https://open.feishu.cn/open-apis/bot/v2/hook/68c79855-f43e-4584-b64a-3b79c62de9f8'
    if j == '':
        return
    payload_message = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "检查结果",
                "content": [
                    [{"tag": "text","text": j}],[{"tag": "a","text": "查看任务","href": jenkins_url}]
                ]
            }
        }
    }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=json.dumps(payload_message))
if __name__ == '__main__':
    text = [{"tag": "text","text": "第一行\n第二行"},{"tag": "a","text": "查看任务","href": None}]
    print(json.loads('{"tag": "text","text": "第一行第二行"}'))
    d = {'tag': 'text', 'text': '第一行第二行'}
    j = json.dumps(d)
    d = [d]
    d[0]['text'] = '1'
    fbSend('**sss** ')