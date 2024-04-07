# Utiliza una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo en /beeUtp
WORKDIR /beeUtp

# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu aplicación a la imagen
COPY . .

# Expone el puerto 8000 para que la aplicación Django sea accesible
EXPOSE 8000

# Agrega un nombre a la instancia
LABEL app="beeutp"

# Correr migraciones de Django
CMD ["python", "manage.py", "migrate"]

# Comando para ejecutar la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
