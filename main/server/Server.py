import paho.mqtt.client as mqtt

from main.config.config import HOST, PORT, publish_topic
from queue import Queue
import datetime
import threading
from threading import Thread, Event
import paho.mqtt.client as mqtt
from main.mysql import *
from abc import abstractmethod


class Server:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(HOST, PORT, 60)
        self.lock = threading.Lock()
        self.loopNum = 0

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

    def serverStart(self):  # 启动进程，使用threading（python自带进程管理库）进行管理
        loopThread = threading.Thread(target=self.start_loop)
        loopThread.start()
        return loopThread

    @abstractmethod
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            client.subscribe('test')  # 订阅 login 主题
        else:
            print("Failed to connect, return code %d\n", rc)

    @abstractmethod
    def on_message(self, client, userdata, msg):
        # 规定传入数据均为dict的形式
        data = eval(msg.payload.decode('utf-8'))
        print(data)
        return data


class Register(Server):
    def __init__(self):
        super().__init__()
        self.serverStart()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            client.subscribe(publish_topic['register_topic'])  # 订阅 register 主题
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        # 规定传入数据均为dict的形式
        data = eval(msg.payload.decode('utf-8'))
        print(data)
        userName = data.get('userName')
        userPwd = data.get('userPwd')
        returnTopic = data.get('returnTopic')
        self.register(userName, userPwd, returnTopic)
        return data

    def register(self, userName, userPwd, returnTopic):
        user = UserManage.chackName(userName)
        if user == None:
            print("用户不存在，允许注册")
            if UserManage.addUser(userName, userPwd):
                print("用户添加成功！")
                data = {'code': 1, "message": "用户添加成功！"}
                self.client.publish(returnTopic, str(data).encode(), 1)
            else:
                print("用户添加失败，错误发生在服务器！")
                data = {'code': 0, "message": "用户添加失败，错误发生在服务器！"}
                self.client.publish(returnTopic, str(data).encode(), 1)
        else:
            print("用户存在，不允许注册")
            data = {'code': 0, "message": "用户添加失败，用户存在"}
            self.client.publish(returnTopic, str(data).encode(), 1)


class Login(Server):
    def __init__(self):
        super().__init__()
        self.serverStart()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            client.subscribe(publish_topic['login_topic'])  # 订阅 login 主题
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        # 规定传入数据均为dict的形式
        data = eval(msg.payload.decode('utf-8'))
        print(data)
        userName = data.get('userName')
        userPwd = data.get('userPwd')
        returnTopic = data.get('returnTopic')
        self.login(userName, userPwd, returnTopic)
        return data

    def login(self, userName, userPwd, returnTopic):
        user = UserManage.chackName(userName)
        if user == None:
            print("账号或密码错误")
            data = {'code': 0, 'message': "账号或密码错误"}
            self.client.publish(returnTopic, str(data).encode(), 1)
        else:
            if UserManage.verifyUser(userName, userPwd):
                print(f"{userName}通过验证，欢迎")
                data = {'code': 1, "message": f"验证通过，欢迎回来{userName}"}
                self.client.publish(returnTopic, str(data).encode(), 1)
            else:
                print("账号或密码错误")
                data = {'code': 0, 'message': "账号或密码错误"}
                self.client.publish(returnTopic, str(data).encode(), 1)


###################################################################
# taoyu
class Like(Server):
    def __init__(self):
        super().__init__()
        self.serverStart()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            client.subscribe('like')
            client.subscribe('login')  # 订阅 login 主题
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        # 规定传入数据均为dict的形式
        if msg.topic == 'like':
            data = eval(msg.payload.decode('utf-8'))
            messageId = data.get('message_id')
            returnTopic = data.get('return_topic')

            if not messageId:
                print("Invalid message format")
                return

            # 更新点赞数量
            new_count = LikeManage.like_message(messageId)

            if new_count is None:
                print(f"Failed to update like count for message ID: {messageId}")
                return

            print(f'处理并新的点赞计数成功')
            # 此处可以输出最高点赞的消息ID
            try:
                top_message_id = LikeModel.select().order_by(LikeModel.count.desc()).get()
                if top_message_id:
                    print(f'Top liked message ID: {top_message_id}')
                else:
                    print('No top liked message found.')
            except Exception as e:
                print(f"Error retrieving top liked message: {e}")


###################################################################################
# jia yikun
class Server_room(Server):
    def __init__(self):
        super().__init__()
        self.serverStart()

    def on_connect(self, client, userdata, flags, rc):

        if rc == 0:
            self.connected = True
            print("Connected successfully")
            client.subscribe('chat')  # 订阅 chat 主题
        else:
            raise Exception("Failed to connect mqtt server.")

    def on_message(self, client, userdata, msg):
        # 接收用户消息
        data = eval(msg.payload.decode('utf-8'))
        message = data.get('message')
        senderId = data.get('senderId')
        print(data)
        chat = ChatManage()
        chat.AddChat(message, senderId)

    def publish_all_msg(self):
        if self.connected:
            chat = ChatManage()
            payload = str(chat.getAllManage())
            return self.client.publish('all_msg', payload=payload, qos=2, retain=False)
        else:
            raise Exception("mqtt server not connected! you may use .start_loop() function to connect to server "
                            "firstly.")


###################################################################################
def main():
    a = Register()  # 进程1，处理注册
    b = Login()  # 进程2，处理登入
    c = Like()


main()
