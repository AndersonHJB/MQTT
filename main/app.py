from flask import Flask, render_template, request, redirect, url_for
from client.Client import Login, Register

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_client = Login(username, password)
        # 这里假设登录状态由 MQTT 消息处理，可能需要一些回调机制来处理响应
        return redirect(url_by('profile'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_client = Register(username, password)
        # 注册状态处理类似登录
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/profile')
def profile():
    # 显示用户信息页面，此处需要适当填充
    return 'Welcome, user!'


if __name__ == '__main__':
    app.run(debug=True)
