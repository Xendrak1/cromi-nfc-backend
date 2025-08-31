from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, pin, nombre=None, saldo=0, tipo_usuario=None, password=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre=nombre, pin=pin, saldo=saldo, tipo_usuario=tipo_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, pin, nombre=None, saldo=0, tipo_usuario=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, pin, nombre, saldo, tipo_usuario, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    pin = models.CharField(max_length=20)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_usuario = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['pin', 'nombre']

    objects = UsuarioManager()

    def __str__(self):
        return self.correo
