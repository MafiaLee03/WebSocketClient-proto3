import os

ProtoPath = r'D:\protocol\protocol\proto'
OutPutPath = r'D:\QAfiles\WebSocketClient\proto'

for dirpath, dirnames, filenames in os.walk(ProtoPath):
    current_dir = dirpath.split(ProtoPath)[1]
    current_OutPutPath = OutPutPath + current_dir
    if not os.path.exists(current_OutPutPath):
        os.mkdir(current_OutPutPath)
    for i in filenames:
        if i.split('.')[1] == 'proto':
            os.system('cd /d {0}&protoc --python_out={1} {2}'.format(dirpath,current_OutPutPath,i))