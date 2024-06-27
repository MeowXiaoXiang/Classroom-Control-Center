from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import secrets
import configparser
import os
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)

clients = {}

# 初始化帳戶配置文件
config_file = 'accounts.ini'
if not os.path.exists(config_file):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'username': '', 'password': ''}
    with open(config_file, 'w') as f:
        config.write(f)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    show_register = request.remote_addr == '127.0.0.1'

    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        config = configparser.ConfigParser()
        config.read(config_file)

        if action == 'login':
            if username in config and config[username]['password'] == hashed_password:
                user = User(id=username)
                login_user(user)
                return redirect(url_for('chat'))
        elif action == 'register' and show_register:
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
                config[username] = {'password': hashed_password}
                with open(config_file, 'w') as f:
                    config.write(f)
                return redirect(url_for('login'))
    return render_template('login.html', show_register=show_register)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/get_clients')
@login_required
def get_clients():
    return jsonify(list(clients.keys()))

@app.route('/send_command', methods=['POST'])
@login_required
def send_command():
    data = request.json
    targets = data.get('targets')
    command = data.get('command')
    timestamp = data.get('timestamp')
    command_message = {
        'timestamp': timestamp,
        'command': command
    }
    if "all" in targets:
        socketio.emit('execute_command', command_message, namespace='/')
        return "命令已廣播到全部電腦。", 200
    else:
        for target in targets:
            if target in clients:
                socketio.emit('execute_command', command_message, room=clients[target], namespace='/')
            else:
                return f"客戶端 {target} 未連接。", 404
        return f"命令已發送到所選客戶端。", 200

@socketio.on('register', namespace='/')
def handle_register(data):
    client_id = data.get('client_id')
    if client_id:
        clients[client_id] = request.sid
        emit('status_update', {'message': f'{client_id} 已連接。'}, broadcast=True, namespace='/')
        emit('clients_update', list(clients.keys()), broadcast=True, namespace='/')
        print(f"客戶端 {client_id} 已連接。")
    else:
        print("客戶端連接時未提供 client_id")

@socketio.on('disconnect', namespace='/')
def handle_disconnect():
    client_id = next((key for key, value in clients.items() if value == request.sid), None)
    if client_id:
        clients.pop(client_id, None)
        emit('status_update', {'message': f'{client_id} 已斷開連接。'}, broadcast=True, namespace='/')
        emit('clients_update', list(clients.keys()), broadcast=True, namespace='/')
        print(f"客戶端 {client_id} 已斷開連接。")

@socketio.on('execute_response', namespace='/')
def handle_execute_response(data):
    response_status = '成功' if "SUCCESS" in data['response'] else '失敗'
    clean_response = data['response'].replace('SUCCESS', '').replace('FAIL', '').strip()
    response_message = f"[{data['timestamp']}] 命令執行{response_status}：\n{data['command']}\n來自 {data['client_id']} 的回應：\n{clean_response}"
    emit('execute_response', {'message': response_message, 'client_id': data['client_id'], 'command': data['command'], 'timestamp': data['timestamp'], 'response': clean_response}, broadcast=True, namespace='/')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
