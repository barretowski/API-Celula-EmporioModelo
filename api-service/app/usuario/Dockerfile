# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia todos os arquivos da célula para dentro do contêiner
COPY . .

# Atualiza o pip e instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta padrão usada pelo Uvicorn
EXPOSE 8000

# Comando padrão para iniciar o serviço com hot-reload desabilitado (modo produção)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
