from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class TB_BEE_CANALES(models.Model):
    idCanal = models.BigAutoField(primary_key=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()  # Cambiar a TextField para permitir texto largo
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE) # Agrega la clave foránea a auth_user

    # Establece manualmente el valor predeterminado para fecha_creacion
    fecha_creacion = models.DateTimeField(default=timezone.now, blank=True)
    
    # Usa auto_now para fecha_actualizacion
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'TB_BEE_CANALES'

class TB_BEE_CAMPOS(models.Model):
    idCampo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    max = models.CharField(max_length=255)
    min = models.CharField(max_length=255)
    tiempo_envio = models.CharField(max_length=255)
    idCanal = models.ForeignKey(TB_BEE_CANALES, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    activo = models.BooleanField(default=True)
    urlName = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'TB_BEE_CAMPOS'
        
class TB_BEE_MEDIDAS(models.Model):
    idMedida = models.BigAutoField(primary_key=True)
    valor = models.FloatField()
    fecha = models.DateTimeField (auto_now_add=True)
    idCampo = models.ForeignKey(TB_BEE_CAMPOS, on_delete=models.CASCADE)

    class Meta:
        db_table = 'TB_BEE_MEDIDAS'

class TB_BEE_GRAFICA(models.Model):
    idGrafica = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    ejeX = models.CharField(max_length=50)
    ejeY = models.CharField(max_length=50)
    color = models.CharField(max_length=15)
    backGround = models.CharField(max_length=15)
    Tipo = models.CharField(max_length=30)
    Datos = models.CharField(max_length=8)
    idCampo = models.ForeignKey(TB_BEE_CAMPOS, on_delete=models.CASCADE)  # Ajusta el on_delete según tus necesidades

    def __str__(self):
        return f"{self.titulo} - urlName: {self.idCampo.urlName}- idGrafica: {self.idGrafica}"

    class Meta:
        db_table = 'TB_BEE_GRAFICA'  # Define el nombre de la tabla en la base de datos