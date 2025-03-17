import subprocess
import sys
import os
import shutil

def start_ollama():
    # Vérifier si la commande "ollama" existe
    if shutil.which("ollama") is None:
        print("La commande 'ollama' n'est pas disponible dans ce container, on passe son démarrage.")
        return

    if sys.platform.startswith("darwin"):
        # macOS : ouvre Terminal via AppleScript
        command = 'tell application "Terminal" to do script "ollama serve"'
        subprocess.Popen(["osascript", "-e", command])
    elif sys.platform.startswith("linux"):
        # Si pas d'affichage graphique (headless/Docker) : exécuter directement la commande
        if os.environ.get("DISPLAY") is None:
            subprocess.Popen(["ollama", "serve"])
        else:
            # Dans un environnement graphique, lancer dans GNOME Terminal
            subprocess.Popen([
                'gnome-terminal', '--', 'bash', '-c', 'ollama serve; exec bash'
            ])
    elif sys.platform.startswith("win"):
        subprocess.Popen(["cmd.exe", "/c", "start", "ollama", "serve"])

def start_solr():
    # Privilégier le répertoire /app/solr s'il existe (installé via le Dockerfile)
    if os.path.exists("/app/solr"):
        solr_dir = "/app/solr"
    else:
        solr_dir = os.path.join(os.path.expanduser("~"), "solr")
    if not os.path.exists(solr_dir):
        print("Le dossier Solr n'existe pas :", solr_dir)
        return

    # Choix de la commande selon la plateforme
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        command = ["bin/solr", "start", "-force"]
    elif sys.platform.startswith("win"):
        command = ["solr", "start"]

    # Se positionner dans le dossier de Solr et lancer la commande
    os.chdir(solr_dir)
    subprocess.Popen(command)

if __name__ == "__main__":
    start_ollama()
    start_solr()