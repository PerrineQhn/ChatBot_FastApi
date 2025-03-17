FROM python:3.11-slim

RUN apt-get update && apt-get install -y default-jre wget tar curl lsof haveged && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV SOLR_VERSION=8.11.2
RUN wget https://archive.apache.org/dist/lucene/solr/${SOLR_VERSION}/solr-${SOLR_VERSION}.tgz && \
    tar xzf solr-${SOLR_VERSION}.tgz && \
    mv solr-${SOLR_VERSION} /app/solr && \
    rm solr-${SOLR_VERSION}.tgz && \
    ln -s /app/solr /root/solr

RUN curl -fsSL https://ollama.com/install.sh | sh

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]