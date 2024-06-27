import socketio
import os
import socket
import time

sio = socketio.Client()

SERVER_HOSTNAME = "SERVER_HOSTNAME"
SERVER_PORT = 8080

def get_server_address():
    try:
        server_ip = socket.gethostbyname(SERVER_HOSTNAME)
        print(f"解析伺服器地址: {server_ip}")
        return f"http://{server_ip}:{SERVER_PORT}"
    except socket.gaierror:
        print("無法解析伺服器主機名。")
        return None

def get_hostname():
    return socket.gethostname()

@sio.event
def connect():
    print('成功連接到伺服器')
    sio.emit('register', {'client_id': get_hostname()})

@sio.event
def connect_error(data):
    print('連接伺服器失敗')

@sio.event
def disconnect():
    print('與伺服器斷開連接')

@sio.on('execute_command')
def on_message(data):
    command = data['command']
    command_with_status = f"{command} 2>&1 && echo SUCCESS || echo FAIL"
    timestamp = data['timestamp']
    print(f"接收到命令: {command}")
    process = os.popen(command_with_status)
    response = process.read()
    process.close()
    print(f"命令執行結果: {response}")
    sio.emit('execute_response', {
        'client_id': get_hostname(),
        'command': command,
        'timestamp': timestamp,
        'response': response
    })

def connect_to_server():
    server_url = get_server_address()
    while server_url:
        try:
            print(f"正在連接到伺服器: {server_url}")
            sio.connect(server_url)
            sio.wait()
        except socketio.exceptions.ConnectionError as e:
            print(f"無法連接到伺服器: {e}")
            print("等待300秒後重新嘗試...")
            time.sleep(300)
        except Exception as e:
            print(f"發生未知錯誤: {e}")
            print("等待300秒後重新嘗試...")
            time.sleep(300)
        else:
            break
    else:
        print("無法連接到伺服器。")

if __name__ == "__main__":
    connect_to_server()
