# 智慧教室指令系統 (Smart Classroom Command System)

## 介紹 (Introduction)

智慧教室指令系統專門為了解決教室管理中的指令下達問題而設計。由於我先前管理的教室缺乏現成的管理系統，且不少的解決方案需要較高的權限配置或複雜設定，為了簡化管理過程，我選擇親自設計了這套系統。

本系統提供多種便利的快捷功能，包括關機、重新啟動、啟動 Chrome 瀏覽器，以及發送 PowerShell 公告等常用按鈕，能有效提升教室管理的效率，適用於多台電腦的集中控制場景。

## 文件結構 (File Structure)

- `server.py`: 伺服器端程式，負責處理用戶請求並將指令傳送至客戶端。
- `client.py`: 客戶端程式，接收伺服器指令並執行相應操作。
- `login.html`: 提供使用者登入的網頁介面，進行身分驗證。
- `chat.html`: 指令中心的網頁介面，用於管理員下達指令並查看執行狀態。

## 套件安裝 (Package Installation)

### 伺服器端 (Server Side)

```bash
pip install Flask Flask-SocketIO Flask-Login
```

### 客戶端 (Client Side)

```bash
pip install python-socketio
```

## 使用說明 (Usage Instructions)

### 伺服器端 (Server Side)

首先，打開 `server.py`，修改以下代碼以設置您要使用的端口號：

```python
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=<YOUR_PORT>, debug=True)
```

然後，在命令行中運行伺服器：

```bash
python server.py
```

### 客戶端 (Client Side)

在使用 `client.py` 之前，需要修改以下代碼以設置伺服器的主機名和端口號：

```python
SERVER_HOSTNAME = "SERVER_HOSTNAME"
SERVER_PORT = <YOUR_PORT>
```

然後，在命令行中運行客戶端：

```bash
python client.py
```

### 使用 PyInstaller 打包 (Packaging with PyInstaller)

#### 客戶端 (Client Side)

```bash
pyinstaller --onefile --noconsole client.py
```

### 設置工作排程器 (Setting Up Task Scheduler)

1. 打開工作排程器，創建一個新的基本任務。
2. 設置觸發器為“登入時”。
3. 設置操作為“啟動程式”，選擇打包好的 `client.exe`。
4. 儲存。

## 使用說明 (Usage)

1. 首先，打開瀏覽器並進入 `127.0.0.1:<YOUR_PORT>`
2. 為了安全性，系統僅允許從 `127.0.0.1` 地址進行註冊
3. 註冊完成後，使用新註冊的帳號登入
4. 登入後，即可對其他客戶端下達指令

## 介面預覽 (Interface Preview)

- **登入頁面 (Login Page)**: 使用者進入系統時的登入介面。用戶需要輸入帳號和密碼進行身份驗證。

  ![Login Page](./markdown_imgs/login_page.png)
- **指令中心頁面 (Command Center Page)**: 登入後的主要操作介面，包含常用功能按鈕以及選擇用戶下命令的輸入框。

  ![Command Page](./markdown_imgs/command_page.png)

## 影片展示 (Demo)

以下是智慧教室指令系統的操作影片，展示系統從伺服器啟動到下達批量指令的完整流程。

[![智慧教室指令系統操作影片](https://img.youtube.com/vi/wL6UWMA-Ha0/0.jpg)](https://youtu.be/wL6UWMA-Ha0)
