from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<body>
    <h2>Test de transfert</h2>
    <input type="file" id="monFichier">
    <button onclick="envoyer()">Envoyer le fichier</button>
    <p id="msg"></p>

    <script>
    async function envoyer() {
        const input = document.getElementById('monFichier');
        const msg = document.getElementById('msg');
        if (input.files.length === 0) return alert("Choisis un fichier !");

        const formData = new FormData();
        formData.append('file', input.files[0]);

        msg.innerText = "Envoi en cours...";
        const res = await fetch('/upload', { method: 'POST', body: formData });
        const txt = await res.text();
        msg.innerText = "Réponse serveur : " + txt;
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
    # LOG DE DÉBUT
    print(">>> TENTATIVE D'UPLOAD REÇUE <<<")
    
    if 'file' not in request.files:
        print("!!! ERREUR : Pas de fichier dans la requête !!!")
        return "Pas de fichier", 400
    
    file = request.files['file']
    if file.filename == '':
        print("!!! ERREUR : Nom de fichier vide !!!")
        return "Nom vide", 400

    # Sauvegarde locale
    filename = file.filename
    save_path = os.path.join('/tmp', filename)
    file.save(save_path)
    
    # LOG DE RÉUSSITE (C'est ça que tu dois chercher dans Render)
    print(f"✅ SUCCÈS : Fichier '{filename}' sauvegardé dans /tmp")
    print(f"Taille du fichier : {os.path.getsize(save_path)} bytes")
    
    return f"Bien reçu : {filename}", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
