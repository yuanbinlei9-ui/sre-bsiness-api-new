
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hello SRE! AIOps Platform is Running Successfully!</h1>"

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    # ⚠️ 导师敲黑板：Docker 里的 Web 服务必须绑定 0.0.0.0！
    # 千万别只写 app.run()，否则 K8s 外部探活探不到，依然会一直杀掉你的 Pod！
    app.run(host='0.0.0.0', port=8080)
