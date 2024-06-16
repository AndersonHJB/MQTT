import paho.mqtt.client as mqtt

from main.config.config import HOST, PORT, publish_topic
from queue import Queue
import datetime
import threading
from threading import Thread, Event
import threading
from queue import Queue
import paho.mqtt.client as mqtt
import time
from abc import abstractmethod


class Client:  # 基类
    def __init__(self, userName=None, userPwd=None):
        self.userName = userName
        self.userPwd = userPwd
        self.lock = threading.Lock()

        self.loopNum = 0
        self.start_evt = None  # 这是一个Event对象，用来查看是否验证成功
        # 自动在初始化的时候进行链接
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(HOST, PORT, 60)

    def start_loop(self):
        # 用线程锁来控制同时仅能一个loop_forever
        if self.loopNum == 0:
            self.lock.acquire()
            print('进程锁加载')
            self.loopNum = 1
            self.client._thread_terminate = False
            self.client.loop_forever()

    def stop_loop(self):
        # 停止这个线程
        if self.loopNum == 1:
            self.lock.release()
            print('进程锁结束!!')
            self.client._thread_terminate = True
            self.loopNum = 0

    @abstractmethod
    def on_connect(self, client, userdata, flags, rc):
        pass

    @abstractmethod
    def on_message(self, client, userdata, msg):
        pass

    def clientStart(self):  # 启动进程，使用threading（python自带进程管理库）进行管理
        loopThread = threading.Thread(target=self.start_loop)
        loopThread.start()
        return loopThread


class Register(Client):
    def __init__(self, userName, userPwd):
        super().__init__(userName, userPwd)
        self.clientStart()
        self.publishRegister()

    def on_connect(self, client, userdata, flags, rc):  # 链接
        if rc == 0:
            print("Connected successfully")
            returnRegister = self.userName + "register"
            client.subscribe(returnRegister)  # 订阅 return 主题
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):  # 接受数据
        # 规定传入数据均为dict的形式

        data = eval(msg.payload.decode('utf-8'))
        # 读取数据
        code = data.get('code')
        message = data.get('message')
        if code == 0:
            print(message)
        if code == 1:
            print(message)
        return data

    def publishRegister(self):
        returnTopic = self.userName + "register"
        # 数据发送特定格式
        data = {'userName': self.userName, 'userPwd': self.userPwd, 'returnTopic': returnTopic}
        # qos1
        self.client.publish(publish_topic["register_topic"], str(data).encode(), 1)
        # client.loop()
        print('发布信息 ', publish_topic['register_topic'], ' 成功')


class Login(Client):
    def __init__(self, userName, userPwd):
        super().__init__(userName, userPwd)
        self.clientStart()
        self.publishLogin()

    def on_connect(self, client, userdata, flags, rc):  # 链接
        if rc == 0:
            print("Connected successfully")
            returnLogin = self.userName + "login"
            client.subscribe(returnLogin)  # 订阅 return 主题
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):  # 接受数据
        # 规定传入数据均为dict的形式

        data = eval(msg.payload.decode('utf-8'))
        # 读取数据
        code = data.get('code')
        message = data.get('message')
        if code == 0:  # 表示登入失败
            print(message)
        if code == 1:  # 表示登入成功
            print(message)
        return data

    def publishLogin(self):
        returnTopic = self.userName + "login"
        # 数据发送特定格式
        data = {'userName': self.userName, 'userPwd': self.userPwd, 'returnTopic': returnTopic}
        # qos1
        self.client.publish(publish_topic["login_topic"], str(data).encode(), 1)
        # client.loop()
        print('发布信息 ', publish_topic['login_topic'], ' 成功')


######################################
# tao yu
class Like(Client):
    def __init__(self, messageId):
        super().__init__()
        self.clientStart()
        self.publish_like(messageId)

    @abstractmethod
    def on_connect(self, client, userdata, flags, rc):
        pass

    @abstractmethod
    def on_message(self, client, userdata, msg):
        pass

    def publish_like(client, messageId):
        data = {'message_id': messageId}
        client.publish(publish_topic['like_topic'], str(data).encode(), 1)
        print(f'发布信息到 {publish_topic["like_topic"]} 成功')


####################################################################
def main():
    Register("aiyc","123")
    Login("6", "123456")


main()
