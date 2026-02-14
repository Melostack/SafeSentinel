FROM python:3.10-slim

WORKDIR /app

# Instalar dependências de sistema essenciais
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar supervisor para gerenciar o bot e a api
RUN pip install --no-cache-dir supervisor

# Copiar o restante do código
COPY . .

# Expor a porta da API do FastAPI (8000) e do Bot se necessário
EXPOSE 8000

# Usar supervisord para rodar o bot e a api simultaneamente
CMD ["supervisord", "-c", "supervisord.conf"]
