from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ==========================================
# 🌟 Dify AIOps 中枢配置
# ==========================================
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
# 你的专属 API Key（已经加上了必要的 Bearer 前缀）
DIFY_API_KEY = "Bearer app-yk25W03Hg3tKM4E9yw0YOKJi"

@app.route('/')
def hello():
    return "<h1>Hello SRE! AIOps Platform is Running Successfully!</h1>"

@app.route('/health')
def health_check():
    return "OK", 200

# 🌟 核心功能：对接 Dify 的 AI 诊断接口
@app.route('/api/v1/ai-advisor', methods=['POST'])
def ai_advisor():
    data = request.json or {}
    error_msg = data.get('error_message', 'Pod处于CrashLoopBackOff状态')

    headers = {
        "Authorization": DIFY_API_KEY,
        "Content-Type": "application/json"
    }
    
    # 按照 Dify 官方文档规范组装 Payload
  # 按照 Dify 官方文档规范组装 Payload
    payload = {
        "inputs": {}, 
        "query": f"作为SRE运维专家，请分析以下K8s报错并给出排查建议：{error_msg}",
        "response_mode": "blocking", # 阻塞模式
        # ⚠️ 删除了 conversation_id，让 Dify 自动创建新会话
        "user": "sre-admin" 
    }

    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        
        dify_result = response.json()
        ai_answer = dify_result.get('answer', 'AI思考被打断，未返回结果')
        
        return jsonify({
            "status": "success", 
            "error_analyzed": error_msg,
            "ai_advice": ai_answer
        }), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error", 
            "message": f"连接 Dify 智能中枢失败，请检查网络或 API Key。详细错误: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
