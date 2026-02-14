from flask import Flask, request, render_template_string
import os
import requests

app = Flask(__name__)

# Ton Webhook Discord
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1386119408769962064/ZCxzxZZojkWKF9aoysn84qenKVn7frpVa9RGFFKn6LvUm8v3DQp_H1Z2D4jldICAwhNH"

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head><title>Analyseur</title></head>
<body>
    <h2>Test de transfert</h2>
    <input type="file" id="f"><button onclick="u()">Envoyer</button>
    <p id="s"></p>
    <script>
    async function u(){
        const i=document.getElementById('f'), s=document.getElementById('s');
        if(!i.files[0]) return;
        const d=new FormData(); d.append('file',i.files[0]);
        s.innerText="Envoi...";
        const r=await fetch('/upload',{method:'POST',body:d});
        s.innerText = r.ok ? "Reçu !" : "Erreur";
    }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        path = os.path.join('/tmp', file.filename)
        file.save(path)
        with open(path, 'rb') as f:
            requests.post(DISCORD_WEBHOOK, files={'file': f})
        os.remove(path)
        return "OK", 200
    return "No file", 400

if __name__ == "__main__":
    # CETTE PARTIE EST CRUCIALE POUR RENDER
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
