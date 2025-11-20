# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del nodo al contenedor
COPY . /app

# Instala las dependencias necesarias
RUN pip install --no-cache-dir flask requests

# Comando por defecto (se sobreescribe en docker-compose)
CMD ["python", "frase.py"]
