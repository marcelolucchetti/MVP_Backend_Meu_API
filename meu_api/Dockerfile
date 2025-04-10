# Dockerfile - meu_api
FROM python:3.9-slim

WORKDIR /meu_api

# Copia os arquivos do projeto
COPY . .

# Define o PYTHONPATH para que os imports funcionem corretamente
ENV PYTHONPATH=/meu_api

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão da API
EXPOSE 5001

# Comando para rodar a API
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]