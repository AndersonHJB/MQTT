from flask import Flask, render_template, request, redirect, url_for
from client.Client import Login, Register  # 导入编写的登录和注册

app = Flask(__name__)  # 创建一个 Flask 应用实例


@app.route('/')  # 定义根路由，默认访问这个路由
def index():
    return redirect(url_for('login'))  # 重定向到登录页面


@app.route('/login', methods=['GET', 'POST'])  # 定义登录路由，支持 GET 和 POST 方法
def login():
    if request.method == 'POST':  # 如果是 POST 请求，处理登录表单数据
        username = request.form['username']  # 从表单获取用户名
        password = request.form['password']  # 从表单获取密码
        login_client = Login(username, password)  # 创建一个登录客户端，用于向 MQTT 发送登录信息
        # 这里假设登录状态由 MQTT 消息处理，可能需要一些回调机制来处理响应
        return redirect(url_for('profile'))  # 登录成功后重定向到用户个人资料页面，临时开发的页面
    return render_template('login.html')  # 如果是 GET 请求，显示登录表单


@app.route('/register', methods=['GET', 'POST'])  # 定义注册路由，支持 GET 和 POST 方法
def register():
    if request.method == 'POST':  # 如果是 POST 请求，处理注册表单数据
        username = request.form['username']  # 从表单获取用户名
        password = request.form['password']  # 从表单获取密码
        register_client = Register(username, password)  # 创建一个注册客户端，用于向 MQTT 发送注册信息
        # 注册状态处理类似登录
        return redirect(url_for('login'))  # 注册成功后重定向到登录页面
    return render_template('register.html')  # 如果是 GET 请求，显示注册表单


@app.route('/profile')  # 定义用户个人资料页面的路由
def profile():
    # 显示用户信息页面，此处需要适当填充
    return 'Welcome, user!'  # 显示欢迎信息，实际开发中应显示用户相关信息


if __name__ == '__main__':
    app.run(debug=True)  # 启动 Flask 应用，开启调试模式
