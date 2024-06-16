from main.config.config import mysql_config
from peewee import *
import bcrypt
import datetime

# 链接数据库
db = MySQLDatabase(mysql_config['db_name'], user=mysql_config['db_user'], password=mysql_config['db_password'],
                   host=mysql_config['db_host'], port=mysql_config['db_port'])


# 数据对象
#######################################################
# 基类
class BaseModel(Model):
    class Meta:
        database = db


# 用户类
class UserModel(BaseModel):
    id = AutoField()
    name = CharField(max_length=64)
    password = CharField(max_length=128)

    class Meta:
        db_table = 'user'


# 信息类
class ChatModel(BaseModel):
    id = AutoField()
    message = TextField()
    senderId = BigIntegerField()
    time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'chat'


# 点赞类
class LikeModel(BaseModel):
    id = AutoField()
    messageId = ForeignKeyField(ChatModel, backref='likes')
    count = IntegerField(default=0)

    class Meta:
        db_table = 'like'


class CreateTable:
    @staticmethod
    def create():
        db.connect()
        db.create_tables([UserModel, ChatModel, LikeModel])


# 用户操作
##########################################
def hash_password(password):
    # 生成盐值
    salt = bcrypt.gensalt()
    # 生成哈希值
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


# 验证密码
def check_password(hashed, password):
    # 验证密码
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


# 用户信息传递
class UserManage:
    @staticmethod
    def chackName(name):  # 检测用户是否存在，不存在则打印提示并返回None，否则返回UserModel
        try:
            user = UserModel.get(UserModel.name == name)
            return user
        except UserModel.DoesNotExist:
            print(f"No user found with name: {name}")
            return None
        except Exception as error:
            print(f"An error occurred: {error}")
            return None

    @staticmethod
    def chackPassword(password):  # 如果密码正确则返回True
        # 密码加密
        hashPassword = hash_password(password)
        return check_password(hashPassword, password)

    @staticmethod
    def addUser(name, password):
        try:
            pwd = hash_password(password)
            UserModel.insert(name=name, password=pwd).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def verifyUser(name, password):
        user = UserManage.chackName(name)
        if user is None:
            return False
        hashed_password_bytes = user.password.encode('utf-8')
        return check_password(hashed_password_bytes, password)


################################################################
class ChatManage:

    # 获取并返回所有 chat 数据
    @staticmethod
    def getAllManage():
        try:
            all_chats = ChatModel.select()
            # 将数据转换为列表形式
            chat_list = []
            for chat in all_chats:
                chat_data = {
                    'id': chat.id,
                    'message': chat.message,
                    'senderId': chat.senderId,
                    'time': chat.time
                }
                chat_list.append(chat_data)
            return chat_list
        except Exception as error:
            print(error)
            return None

    @staticmethod
    def AddChat(message, senderId):
        try:
            ChatModel.insert(message=message, senderId=senderId).execute()
            return 'Succeed'
        except Exception as error:
            print(error)
            return 'Fail'


#################################################################
# taoyu:
class LikeModel(BaseModel):
    id = AutoField()
    messageId = ForeignKeyField(ChatModel, backref='likes')
    count = IntegerField(default=0)

    class Meta:
        db_table = 'like'


def display_all_users():
    try:
        users = UserModel.select()
        user_list = []

        for user in users:
            last_message = ChatModel.select().where(ChatModel.senderId == user.id).order_by(
                ChatModel.time.desc()).first()
            if last_message:
                last_message_time = last_message.time
            else:
                last_message_time = "No messages found"

            user_data = {
                "id": user.id,
                "name": user.name,
                "last_message_time": last_message_time
            }
            user_list.append(user_data)

        print(f"Total users: {len(user_list)}")
        print("User list:", user_list)
    except Exception as error:
        print(f"An error occurred while fetching users: {error}")


class LikeManage:
    @staticmethod
    def like_message(messageId):
        try:
            like, created = LikeModel.get_or_create(messageId=messageId, defaults={'count': 0})
            if not created:
                like.count += 1
                like.save()
            return like.count
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
