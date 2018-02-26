#!/usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'tiany'
__date__ = '2018/2/26 16:42'


import itchat,time,re
from itchat.content import *

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def tuling_reply(msg):
    # 获取对方输入
    match = re.search(u"年",msg.text).span()
    if  match:
        itchat.send((u"狗年汪汪汪"),msg['FromUserName'])
    # 如果匹配成功则回复

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    itchat.send((u"狗年汪汪汪"),msg['FromUserName'])
# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
#itchat.auto_login(hotReload=True,enableCmdQR=True)
itchat.run()
