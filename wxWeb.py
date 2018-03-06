#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
import hashlib
import sys
import wxTools
from wxTools import wxLog
from lxml import etree
import wxMsg

urls = (
    '/', 'index'
)


class index:
    def GET(self):
        '''
        GET貌似只有验证Token
        :return:
        '''
        getData = web.input()
        wxLog("GET:\n"+getData)
        text = token(getData)
        if text != "":
            return text

        return 0


    def POST(self):
        '''
        收取信息之类的
        :return:
        '''
        postData = web.data()
        str_xml = postData.decode("utf-8")
        xml = etree.fromstring(str_xml)
        ToUserName = xml.find("ToUserName").text
        FromUserName = xml.find("FromUserName").text

        msgType = xml.find("MsgType").text

        if msgType == "text":
            '''
            普通消息
            '''
            content = xml.find("Content").text
            wxLog('收到{}:{} '.format(msgType, content))
            text = wxMsg.textMsg(ToUserName,FromUserName,content)

        if msgType == "image":
            PicUrl = xml.find("PicUrl").text
            text = wxMsg.imageMsg(ToUserName,FromUserName,PicUrl)

        if msgType == "event":
            #事件
            Event = xml.find("Event").text
            text = wxMsg.subscribeEvent(ToUserName,FromUserName,Event)


        # printRed()


        return text


def token(data):
    if len(data) == 0:
        return "len is 0"

    try:
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
    except TypeError as e:
        return ""


    token = '******' #token
    list = [token, timestamp, nonce]
    list.sort()
    text = list[0] + list[1] + list[2]
    sha1 = hashlib.sha1()
    # map(sha1.update, text.encode("utf-8"))
    sha1.update(text.encode("utf-8"))
    hashcode = sha1.hexdigest()

    wxLog("收到Token验证:     func: hashcode, signature: "+hashcode+"   "+signature)
    if hashcode == signature:
        wxLog("验证成功")
        return echostr
    else:
        wxLog("验证失败")
        return ""





if __name__ == "__main__":
    wxLog("-----------------------启动服务-----------------------")
    app = web.application(urls, globals())
    app.run()