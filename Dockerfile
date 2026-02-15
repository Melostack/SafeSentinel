FROM python:3.11-slim

WORKDIR /app

# Instala dependências de sistema necessárias para algumas libs python
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements da raiz para dentro da pasta api durante o build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando para rodar a API
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
