# ChatBot_FastApi

**Auteurs :** LI Zhongjie & QUENNEHEN Perrine

---

**Chatbot IA** est une application web basée sur **FastAPI** permettant d'interagir avec un chatbot intelligent. Le projet propose :

- **Interface web interactive :** Templates HTML avec Jinja2, style CSS moderne et interactions JavaScript intuitives (auto-scroll, envoi via Entrée, etc.).
- **Gestion contextuelle des conversations :** Maintien de l'historique des échanges pour améliorer la pertinence des réponses.
- **Indexation des échanges avec Solr :** Enregistrement des conversations dans Solr pour faciliter les recherches ultérieures.
- **Lancement automatique des services :** Démarrage automatique des serveurs Solr et Ollama via un script d'entrée (`entrypoint.sh`).

---

## Table des matières

- [Prérequis](#prérequis)
- [Structure du projet](#structure-du-projet)
- [Installation avec Docker](#installation-avec-docker)
- [Installation manuelle](#installation-manuelle)
- [Lancement manuel](#lancement-manuel)
- [Configuration](#configuration)
- [Fonctionnalités](#fonctionnalités)

---

## Prérequis

- **Docker** (recommandé)

Sinon, pour une installation manuelle :

- **Python 3.12** ou supérieur
- **Solr 8.11.2**
- **Ollama**
- Packages Python :
  - FastAPI
  - Uvicorn
  - Jinja2
  - Pydantic
  - pysolr
  - ollama

---

## Structure du projet

```
ChatBot_FastApi/
├── app.py                     # Application FastAPI principale
├── qa.json                    # Historique des échanges sauvegardé (dans static)
├── dockerfile                 # Instructions pour créer l'image Docker
├── entrypoint.sh              # Script de lancement automatique des services
├── requirements.txt           # Dépendances Python
├── templates/                 # Templates HTML
│   ├── index.html             # Page d'accueil
│   ├── chat.html              # Affichage des échanges
│   └── chatlogs.html          # Page d'historique des logs
├── static/                    # Ressources statiques
│   ├── __init__.py            # Module d'initialisation
│   ├── style.css              # Styles CSS
│   ├── script.js              # Scripts JS pour interactions
│   ├── open_app.py            # Fonctions pour démarrer Solr et Ollama
│   └── logo.svg               # Logo du chatbot
└── chatlogs.zip               # Configuration Solr pour le core "chatlogs"
```

> **Note :** `qa.json` est automatiquement géré par l'application.

---

## Installation avec Docker

**1. Construire l'image Docker :**

```bash
docker build -t chatbot_fastapi .
```

**2. Exécuter l'application via Docker :**

```bash
docker compose up --build
```

Accès : [http://localhost:8001](http://localhost:8001)

**3. Vérification de la connexion au serveur**

```bash
curl http://localhost:8001
```

---

## Installation manuelle

**1. Cloner le dépôt :**

```bash
git clone https://github.com/PerrineQhn/ChatBot_FastApi
cd ChatBot_FastApi
```

**2. Installer les dépendances Python :**

```bash
pip install -r requirements.txt
```

**3. Installer Ollama :**

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3.2
```

**4. Installer Apache Solr :**

```bash
wget https://archive.apache.org/dist/lucene/solr/8.11.2/solr-8.11.2.tgz
tar xzf solr-8.11.2.tgz
solr-8.11.2/bin/solr start
solr-8.11.2/bin/solr create -c chatlogs
```

---

## Lancement manuel

Lancer FastAPI depuis la racine du projet :

```bash
uvicorn app:app
```

Application accessible via [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Configuration

- **Templates et statiques :** situés dans `templates` et `static`.
- **Services externes (Solr, Ollama) :**
  - Modifiables via `static/open_app.py`.
- **Historique des échanges :**
  - Stockage JSON (`qa.json`).
  - Indexation Solr automatique.

---

## Fonctionnalités

- **Interface moderne et responsive** : HTML/CSS/JS adaptable et intuitive.
- **Conversation contextuelle** : historique utilisé par l'IA.
- **Indexation avec Solr** : simplification des recherches sur les conversations.
- **Services automatisés** : démarrage simultané et automatique de Solr et Ollama à chaque lancement via Docker ou le script d'entrée (`entrypoint.sh`).
