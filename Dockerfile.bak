FROM python:3.10-slim

WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y 
    curl 
    gnupg 
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - 
    && apt-get install -y nodejs 
    && rm -rf /var/lib/apt/lists/*

# Instalar n8n globalmente
RUN npm install -g n8n

# Copiar arquivos do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose only n8n port
EXPOSE 5678

# Usar supervisord para rodar múltiplos processos se necessário, 
# mas no Render/Koyeb seguiremos o supervisord.conf
RUN pip install supervisor

CMD ["supervisord", "-c", "supervisord.conf"]
