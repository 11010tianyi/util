#!/usr/bin/env python
# _*_ coding: utf-8 _*_
__author__ = 'tiany'
__date__ = '2018/2/26 16:42'


import itchat,time,re,requests,random
from itchat.content import *

replied = []
# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def tuling_reply(msg):
    if u"年" in msg.text and msg['FromUserName'] not in replied:
        sendGreeting(msg)

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def other_reply(msg):
    if msg['FromUserName'] not in replied:
        sendGreeting(msg)


def sendGreeting(msg):
    global replied
    friend = itchat.search_friends(userName=msg['FromUserName'])
    itchat.send((friend['RemarkName']+" "+ getRandomGreeting()),msg['FromUserName'])
    replied.append(msg['FromUserName'])

greeting_list = [u'汪汪汪',u"喵喵喵",u"唧唧基",u"嘎嘎嘎","happy new year"]
length_list = len(greeting_list)
def  getRandomGreeting():
    index = int(random.random()*3)
    greeting = greeting_list[index]
    return greeting

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
#itchat.auto_login(hotReload=True,enableCmdQR=True)
itchat.run()
