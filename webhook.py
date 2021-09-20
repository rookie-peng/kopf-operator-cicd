import os
import json
import random
import requests
from flask import Flask
from flask import request, jsonify, abort

app = Flask(__name__)
WEBHOOK_VERIFY_TOKEN = "easycicd"

# 指明想要触发哪个命名空间的easycicd资源
namespace = os.environ.get('namespace', 'default')
# token = os.popen('cat /var/run/secrets/kubernetes.io/serviceaccount/token').read()
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRUSGpZVWI1c2lvZ2U2YXBVbnh3WkFvXzQzbFVybHBWNUV2Wlp6aFFyNWcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFkbWluLXNhLXRva2VuLTY5bmQ0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXNhIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMGM1YTY5MTktYzZkOS00MjI5LTkzMGUtMmFkNWIxYmMyY2U2Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6YWRtaW4tc2EifQ.bF6q3PdBecnC3F_NUIlDctar8L6ZX22h7ggdDwiitYz4-oW-hUTlIjFgTBnuUETxyT_jXGWjupLaROm75qj2S5WJsGwgP-vAzR5JrMvbH3DAZI6W1A_k7UkhNFSBHC7MEY1n9sa3SWQJEsQ89CZ6eqVxtxymdw4B8J_ZHpZKosxqMoo3EH2pGHTvplx3-aSHbz_drldi_F0seGDK-afeA1cfrH9p4ZN1m7XfBUDWBXlkvucaR7A3XIuKkNOgxmjN60-WLKo03jnLOyezRRMDLCaxI56rijySBY0a4rNQDQ8oWvwxzBiHPRhgZIaELud8w6tjj_4prT6ls0uaAQh-Jw"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.headers.get('X-Gitlab-Token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad token'}), 401

    elif request.method == 'POST':
        verify_token = request.headers.get('X-Gitlab-Token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            try:
                data = json.loads(request.get_data(as_text=True))
                user = data['user_username']
                app = data['project']['name']

                # 触发easycicd的变更，引起重新cicd的动作进行应用变更。注意如果没有创建easycicd资源则会抛异常。
                # url = f'https://kubernetes:443/apis/rootcloud.com/v1/namespaces/{namespace}/easycicd/app'
                url = 'https://10.70.40.110:6443/apis/rootcloud.com/v1/namespaces/default/easycicd/nginx-1-cicd'
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/merge-patch+json',
                    'Authorization': 'Bearer ' + token,
                }
                body = json.dumps({"spec": {"resourceVersion": random.randint(0, 9999)}})
                response = requests.patch(url, data=body, headers=headers, verify=False)

                print(json.dumps(json.loads(response.text), indent=4))
                print(user, app)
                return jsonify({'status': 'success'}), 200
            except Exception as e:
                print(e.message)
                return jsonify({'status': 'bad result'}), 500
        else:
            return jsonify({'status': 'bad token'}), 401

    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
