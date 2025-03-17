FROM python:3.11-slim

WORKDIR /app

# Copier les fichiers en premier
COPY . /app

# Installer les dépendances système, y compris curl et ping
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    iputils-ping \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'application
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]