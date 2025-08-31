from django.db import models
import uuid
from usuarios.models import Usuario

class Recarga(models.Model):
    id_recarga = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField()
    metodo = models.CharField(max_length=50)

    def __str__(self):
        return f"Recarga {self.id_recarga} - Usuario {self.id_usuario}"
