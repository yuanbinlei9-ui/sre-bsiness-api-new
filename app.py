from flask import Flask, request, jsonify
import requests
import json  # 🌟 务必新增这个包，用来解析流式 JSON 数据

app = Flask(__name__)

DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = "Bearer app-yk25W03Hg3tKM4E9yw0YOKJi"

@app.route('/')
def hello():
    return "<h1>Hello SRE! AIOps Platform is Running Successfully!</h1>"

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/api/v1/ai-advisor', methods=['POST'])
def ai_advisor():
    data = request.json or {}
    error_msg = data.get('error_message', 'Pod处于CrashLoopBackOff状态')

    headers = {
        "Authorization": DIFY_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {}, 
        "query": f"作为SRE运维专家，请分析以下K8s报错并给出排查建议：{error_msg}",
        "response_mode": "streaming", # 🌟 核心修改 1：顺应 Dify 的要求，改为流式模式
        "user": "sre-admin" 
    }

    try:
        # 🌟 核心修改 2：加上 stream=True，告诉 Python 我们要接收流式数据
        response = requests.post(DIFY_API_URL, headers=headers, json=payload, stream=True)
        response.raise_for_status() 
        
        ai_answer = ""
        # 🌟 核心修改 3：像 SRE 拼凑碎片一样，把大模型吐出的 SSE (Server-Sent Events) 数据流拼接起来
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    try:
                        json_data = json.loads(decoded_line[6:])
                        # 兼容基础聊天和 Agent 两种模式的返回体
                        if json_data.get('event') in ['message', 'agent_message']:
                            ai_answer += json_data.get('answer', '')
                    except json.JSONDecodeError:
                        continue
        
        return jsonify({
            "status": "success", 
            "error_analyzed": error_msg,
            "ai_advice": ai_answer
        }), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error", 
            "message": f"连接 Dify 失败: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
