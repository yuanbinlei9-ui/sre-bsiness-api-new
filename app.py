from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ==========================================
# 🌟 Dify AIOps 中枢配置
# ==========================================
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = "Bearer app-yk25W03Hg3tKM4E9yw0YOKJi"

# ==========================================
# 🎨 极客暗黑风的前端 HTML 界面
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>GenAI SRE 智能运维诊断平台</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; padding: 40px; }
        .container { max-width: 800px; margin: 0 auto; background-color: #313244; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { text-align: center; color: #89b4fa; }
        .subtitle { text-align: center; color: #a6adc8; margin-bottom: 30px; }
        textarea { width: 100%; height: 150px; background-color: #181825; color: #a6e3a1; border: 1px solid #45475a; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 14px; resize: vertical; box-sizing: border-box; margin-bottom: 20px; }
        textarea:focus { outline: none; border-color: #89b4fa; }
        button { width: 100%; padding: 15px; background-color: #89b4fa; color: #1e1e2e; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background-color 0.3s; }
        button:hover { background-color: #b4befe; }
        button:disabled { background-color: #45475a; color: #a6adc8; cursor: not-allowed; }
        #result { margin-top: 30px; padding: 20px; background-color: #181825; border-radius: 8px; border-left: 4px solid #a6e3a1; display: none; line-height: 1.6; }
        .loading { text-align: center; font-style: italic; color: #f38ba8; margin-top: 20px; display: none; font-weight: bold; }
        /* 优化 Markdown 渲染后的样式 */
        #result h3 { color: #f9e2af; margin-top: 0; }
        #result code { background-color: #313244; padding: 2px 6px; border-radius: 4px; color: #fab387; }
        #result pre code { display: block; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 GenAI 云原生智能运维诊断中枢</h1>
        <p class="subtitle">请输入 K8s 集群日志或应用报错，大模型将为您进行根因分析并输出自愈建议。</p>
        
        <textarea id="errorInput" placeholder="请输入你的报错信息，例如：K8s Pod 处于 CrashLoopBackOff 状态，Exit Code 是 137..."></textarea>
        
        <button id="submitBtn" onclick="diagnose()">一键召唤 AI 专家诊断</button>
        
        <div id="loading" class="loading">🧠 SRE 专家模型正在深度思考中，请稍候...</div>
        
        <div id="result"></div>
    </div>

    <script>
        async function diagnose() {
            const input = document.getElementById('errorInput').value;
            if (!input) {
                alert("请先输入报错日志！");
                return;
            }

            const btn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const resultDiv = document.getElementById('result');

            // UI 状态切换：按钮变灰，显示加载动画
            btn.disabled = true;
            btn.innerText = "诊断中...";
            resultDiv.style.display = 'none';
            loading.style.display = 'block';

            try {
                // 发送数据给咱们的 Flask 后端接口
                const response = await fetch('/api/v1/ai-advisor', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ error_message: input })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // 使用 marked.js 将 Markdown 渲染为漂亮格式
                    resultDiv.innerHTML = marked.parse(data.ai_advice);
                    resultDiv.style.display = 'block';
                } else {
                    resultDiv.innerHTML = `<span style="color: #f38ba8;">诊断失败：${data.message}</span>`;
                    resultDiv.style.display = 'block';
                }
            } catch (error) {
                resultDiv.innerHTML = `<span style="color: #f38ba8;">网络请求错误：${error.message}</span>`;
                resultDiv.style.display = 'block';
            } finally {
                // 恢复 UI 状态
                btn.disabled = false;
                btn.innerText = "一键召唤 AI 专家诊断";
                loading.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/health')
def health_check():
    return "OK", 200

# ==========================================
# 🧠 核心 API：对接大模型，支持网页与监控告警双轨输入
# ==========================================
@app.route('/api/v1/ai-advisor', methods=['POST'])
def ai_advisor():
    data = request.json or {}
    
    # 🌟 核心升级：AIOps 智能路由与格式自适应解析
    if 'alerts' in data and len(data['alerts']) > 0:
        # 路线 A：如果是 Prometheus Alertmanager 自动触发的 Webhook 告警
        alert = data['alerts'][0] # 提取第一条核心告警
        labels = alert.get('labels', {})
        annotations = alert.get('annotations', {})
        
        alert_name = labels.get('alertname', '未知监控告警')
        pod_name = labels.get('pod', '未知Pod')
        description = annotations.get('description', annotations.get('message', '无详细描述'))
        
        # 组装成大模型能听懂的 SRE 报错日志
        error_msg = f"监控系统触发告警 [{alert_name}]！影响的Pod为 [{pod_name}]。详细报错信息：{description}"
    else:
        # 路线 B：如果是人类工程师在前端控制台手动输入的排障日志
        error_msg = data.get('error_message', 'Pod处于CrashLoopBackOff状态')

    headers = {
        "Authorization": DIFY_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {}, 
        "query": f"作为SRE运维专家，请分析以下K8s报错并给出排查建议：{error_msg}",
        "response_mode": "streaming", 
        "user": "sre-admin" 
    }

    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=payload, stream=True)
        response.raise_for_status() 
        
        ai_answer = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    try:
                        json_data = json.loads(decoded_line[6:])
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
        return jsonify({"status": "error", "message": f"连接 Dify 失败: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
