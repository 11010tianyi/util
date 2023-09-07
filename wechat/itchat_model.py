#!/usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'tiany'
__date__ = '2018/2/14 20:38'

#!/usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'tiany'
__date__ = '2018/2/14 7:51'


import itchat,time
import requests
from itchat.content import *

KEY = 'bde97a94303c4b248a30474548503477'
def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'

    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'worldoftianyi',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        # return r.get('text')
        if type(msg) == str:
            return r.get('text')
        else:
            return r.get()
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = u'我听到你在说: ' + msg.text
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg.text)
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    files = msg.download(msg.fileName)
    reply = get_response(files)
    defaultReply = u'我听到你在说: ' + msg.fileName
    return reply or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True,enableCmdQR=True)
itchat.run()
