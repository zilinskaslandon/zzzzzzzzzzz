from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

# ========== 初始化数据库 ==========
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  content TEXT,
                  contact TEXT,
                  time TEXT)''')
    conn.commit()
    conn.close()

# ========== 脚本列表（你在这里维护你的脚本） ==========
SCRIPTS = [
    {
        "id": "001",
        "name": "自动农场V3",
        "version": "3.2",
        "description": "支持最新地图，自动收菜",
        "download_url": "https://raw.githubusercontent.com/你的用户名/仓库名/main/你的脚本.lua"
    },
    {
        "id": "002",
        "name": "跑酷辅助",
        "version": "1.5",
        "description": "自动避障 + 加速",
        "download_url": "https://raw.githubusercontent.com/你的用户名/仓库名/main/你的脚本2.lua"
    }
]

# ========== API 接口 ==========

# 1. 获取脚本列表
@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    return jsonify({"code": 200, "data": SCRIPTS})

# 2. 提交反馈
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    content = data.get('content', '').strip()
    contact = data.get('contact', '').strip()
    
    if not content:
        return jsonify({"code": 400, "message": "内容不能为空"})
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (content, contact, time) VALUES (?,?,?)",
              (content, contact, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    
    return jsonify({"code": 200, "message": "感谢反馈！已收到"})

# 3. 健康检查
@app.route('/')
def health():
    return "API 运行正常 ✅"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
