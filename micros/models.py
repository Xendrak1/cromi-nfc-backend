from django.db import models
import uuid

# Create your models here.

class Gremialista(models.Model):
    id_gremialista = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Micro(models.Model):
    id_micro = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    linea = models.CharField(max_length=50)
    placa = models.CharField(max_length=50)
    gremialistas = models.ManyToManyField(Gremialista, through='MicroGremialista')

    def __str__(self):
        return self.placa

class MicroGremialista(models.Model):
    id_micro = models.ForeignKey(Micro, on_delete=models.CASCADE)
    id_gremialista = models.ForeignKey(Gremialista, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_micro', 'id_gremialista')
