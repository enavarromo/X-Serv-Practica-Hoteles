from django.db import models

# Create your models here.

class Usuario(models.Model):
    Nombre = models.CharField(max_length=50, primary_key=True)
    TituloPagina = models.CharField(max_length=50)
    Letra = models.IntegerField()
    ColorFondo = models.CharField(max_length=50)  # Antes IntegerField

class Alojamiento(models.Model):
    # Basic Data:
    Nombre = models.CharField(max_length=50)
    Telefono = models.CharField(max_length=50)
    Descripcion = models.TextField()
    URL = models.CharField(max_length=255)
    # Geo Data:
    Direccion = models.CharField(max_length=50)
    Latitud = models.CharField(max_length=50)   # Nuevo
    Longitud = models.CharField(max_length=50)  # Nuevo
    # Extra data:
    Categoria = models.CharField(max_length=255)
    SubCategoria = models.CharField(max_length=255)
    # Mine data:
    Usuario = models.ManyToManyField('Usuario')
    NumeroComentarios = models.IntegerField()  # Por comodidad: coger los 10 con mas comentarios
    
class Foto(models.Model):
    Alojamiento = models.ForeignKey('Alojamiento', on_delete=models.CASCADE)
    URL = models.CharField(max_length=255)

class Comentario(models.Model):
    Alojamiento = models.ForeignKey('Alojamiento', on_delete=models.CASCADE)
    Usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)    # Nuevo
    Descripcion = models.TextField()

class FechaSeleccion(models.Model):
    Alojamiento = models.ForeignKey('Alojamiento', on_delete=models.CASCADE)
    Usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    Fecha = models.DateTimeField(auto_now=False, auto_now_add=False)



# Old:
class Pages(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    page = models.TextField()


# En Alojamiento, modificaciones:
#    MiniImagenURL = models.CharField(max_length=255)    # Demomento link a la miniImagen TBD
