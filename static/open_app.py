import subprocess
import sys
import os

def start_ollama():
    if sys.platform.startswith("darwin"):
        # Ouvre l'application Terminal et exécute "ollama serve"
        command = 'tell application "Terminal" to do script "ollama serve"'
        subprocess.Popen(["osascript", "-e", command])
    elif sys.platform.startswith("linux"):
        # Ouvre GNOME Terminal et exécute "ollama serve", puis garde le terminal ouvert
        subprocess.Popen([
            'gnome-terminal', '--', 'bash', '-c', 'ollama serve; exec bash'
    ])
    elif sys.platform.startswith("win"):
        # Ouvre le terminal Windows et exécute "ollama serve"
        subprocess.Popen(["cmd.exe", "/c", "start", "ollama", "serve"])

def start_solr():
    if sys.platform.startswith("darwin"):
        # macOS
        solr_dir = os.path.join(os.path.expanduser("/opt/homebrew/bin/"))
        command = ["solr", "start"]  # commande à exécuter depuis le dossier Solr
    elif sys.platform.startswith("linux"):
        # Linux
        solr_dir = os.path.join(os.path.expanduser("~"), "solr")
        command = ["bin/solr", "start"]

    if not os.path.exists(solr_dir):
        print("Le dossier Solr n'existe pas :", solr_dir)
        return

    # Exécute la commande depuis le dossier Solr
    os.chdir(solr_dir)
    subprocess.Popen(command)

if __name__ == "__main__":
    start_ollama()
    start_solr()