# Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y default-jre wget curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Installation Solr
RUN wget https://archive.apache.org/dist/lucene/solr/8.11.2/solr-8.11.2.tgz && \
    tar xzf solr-8.11.2.tgz && mv solr-8.11.2 /app/solr && rm solr-8.11.2.tgz

# Installer Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Exposer le port de l'app
EXPOSE 8000

# Volume pour persistance Ollama et Solr
VOLUME ["/root/.ollama", "/app/solr/server/solr"]

# Copier les fichiers et entrypoint
COPY . /app
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]