#!/bin/bash

# Démarrage du service Ollama
echo "Démarrage du service Ollama..."
ollama serve &

# Attendre qu'Ollama démarre complètement
sleep 5

# Vérifier si le modèle llama3.2 est déjà téléchargé
if ! ollama list | grep -q "llama3.2"; then
    echo "Pull du modèle llama3.2..."
    ollama pull llama3.2
else
    echo "Modèle llama3.2 déjà téléchargé."
fi

# Démarrer Solr avec l'option -force
echo "Démarrage de Solr..."
/app/solr/bin/solr start -force

# Vérifier si le core chatlogs existe, sinon le créer
if ! /app/solr/bin/solr status | grep -q "chatlogs"; then
    echo "Création du core 'chatlogs'..."
    /app/solr/bin/solr create_core -c chatlogs -n data_driven_schema_configs -force
else
    echo "Le core 'chatlogs' existe déjà."
fi

echo "Démarrage de l'application FastAPI..."
exec uvicorn app:app --host 0.0.0.0 --port 8000
