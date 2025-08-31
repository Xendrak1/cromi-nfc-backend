from django.db import models
import uuid
from usuarios.models import Usuario
from micros.models import Micro

class Pago(models.Model):
    id_pago = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_micro = models.ForeignKey(Micro, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago {self.id_pago} - Usuario {self.id_usuario}"
