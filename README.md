# ChatBot_FastApi

Auteurs : LI Zhongjie & QUENNEHEN Perrine

---

Chatbot IA est une application web basée sur FastAPI qui propose un chatbot intelligent. Le projet intègre plusieurs fonctionnalités :

- **Interface web interactive** : Utilisation de Jinja2 pour les templates HTML, CSS pour le style moderne et JavaScript pour les interactions (auto-scroll, envoi via la touche Entrée, etc.).
- **Gestion du contexte de conversation** : Le chatbot garde en mémoire l'historique de la conversation afin d'améliorer la pertinence des réponses.
- **Indexation des échanges avec Solr** : Les échanges sont indexés dans Solr pour permettre de rechercher facilement l'historique.
- **Lancement automatique de services** : Le module `open_app.py` permet de démarrer automatiquement le serveur Solr et le serveur Ollama au démarrage de l'application.

---

## Table des matières

- [Prérequis](#prérequis)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement de l'application](#lancement-de-lapplication)
- [Fonctionnalités](#fonctionnalités)
- [Dépannage](#dépannage)
- [Licence](#licence)

---

## Prérequis

- **Python 3.12** (ou version compatible)
- Les packages Python suivants :
  - FastAPI
  - Uvicorn
  - Jinja2
  - Pydantic
  - pysolr
  - ollama
- **Solr** installé et configuré (le core `chatlogs` doit être accessible sur `localhost:8983`)
- **Ollama** installé et accessible via la commande `ollama serve`

---

## Structure du projet

La structure du projet ressemble à :

```
ChatBot_FastApi/
├── app.py                 # Application FastAPI principale
├── qa.json                # Fichier JSON pour sauvegarder l'historique des échanges (géré dans static)
├── requirements.txt       # Liste des dépendances Python
├── templates/             # Dossier des templates HTML
│   ├── index.html         # Page principale du chatbot
│   └── chat.html          # Template d'affichage des échanges
├── static/                # Fichiers statiques (CSS, JavaScript, images, etc.)
│   ├── style.css          # Feuille de style pour l'interface
│   ├── script.js          # Script JavaScript pour les interactions (auto-scroll, etc.)
│   ├── open_app.py        # Module pour lancer Solr et Ollama
│   └── logo.svg           # Logo du chatbot
└── chatlogs.zip           # Dossier contenant les fichiers pour solr (à dézipper et à copier-coller dans son dossier solr)
    
```

> **Note :** Le fichier `qa.json` peut être créé ou vidé automatiquement par l'application. Il est situé dans le dossier `static`.

---

## Installation

1. **Clonez le dépôt :**

   ```bash
   git clone https://github.com/PerrineQhn/ChatBot_FastApi
   cd ChatBot_FastApi
   ```

2. **Créez un environnement virtuel (optionnel mais recommandé) :**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installez les dépendances :**

   Installer le fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

   Sinon, installez manuellement :

   ```bash
   pip install fastapi uvicorn jinja2 pydantic pysolr ollama
   ```

   Installer également le modèle llama3.2 de Ollama :

   ```bash
   ollama run llama3.2
   ```

---

## Configuration

- **Templates et fichiers statiques**  
  L'application est configurée pour rechercher les templates dans le dossier `templates` et les fichiers statiques dans le dossier `static`.  

- **Solr et Ollama**  
  Le module `static/open_app.py` contient les fonctions `start_solr()` et `start_ollama()` qui démarrent les services externes.  
  Vous pouvez modifier ces fonctions selon votre configuration (par exemple, en utilisant un chemin absolu pour Ollama ou en adaptant la commande de lancement de Solr).

- **Gestion du contexte de conversation**  
  Les échanges sont stockés dans un fichier JSON (`qa.json`) et indexés dans Solr. Le contexte de la conversation est conservé dans une variable globale pour la démonstration.

---

## Lancement de l'application

Pour lancer l'application (soyez dans le dossier `ChatBot_FastApi/`):

```bash
uvicorn app:app --reload
```

L'application sera accessible à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000) (indiqué dans le terminal).

Lors du démarrage, le gestionnaire de durée de vie (via un `lifespan`) appelle les fonctions du module `open_app.py` pour démarrer Solr et Ollama.

---

## Fonctionnalités

- **Interface utilisateur moderne et responsive** :  
  L'interface est construite avec HTML, CSS et JavaScript. Elle s'adapte aux différents écrans et propose une expérience utilisateur fluide.

- **Conversation contextuelle** :  
  L'historique de la conversation est transmis au modèle AI pour améliorer la pertinence des réponses.

- **Indexation des échanges dans Solr** :  
  Chaque échange est indexé dans Solr, ce qui permet une recherche et une analyse ultérieure des conversations.

- **Démarrage automatique des services** :  
  Au lancement de l'application, le serveur Solr et le serveur Ollama sont démarrés automatiquement via des fonctions Python dans `open_app.py`.
