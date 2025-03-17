#!/bin/bash
set -e

# Démarrer le service Ollama en arrière-plan (si nécessaire)
echo "Démarrage du service Ollama..."
ollama serve &
sleep 10

# Pull du modèle (optionnel, selon votre logique)
echo "Pull du modèle llama3.2..."
ollama pull llama3.2

# Démarrer le serveur Solr en arrière-plan s'il n'est pas déjà lancé
echo "Démarrage de Solr..."
/app/solr/bin/solr start -force -f &
# Attendre que Solr soit prêt (ajustez le délai si nécessaire)
sleep 15

# Créer le core "chatlogs" si nécessaire
echo "Création du core 'chatlogs'..."
/app/solr/bin/solr create -force -c chatlogs -p 8983 -n data_driven_schema_configs || echo "Le core 'chatlogs' existe déjà."

# Lancer l'application FastAPI
echo "Démarrage de l'application FastAPI..."
exec uvicorn app:app --host 0.0.0.0 --port 8000