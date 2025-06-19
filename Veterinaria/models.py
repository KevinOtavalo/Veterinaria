from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil')
    nombre_completo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    edad = models.PositiveIntegerField()
    rut = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.user.username})"


# Modelo de Mascota
class Mascota(models.Model):
    ESPECIES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIES)
    raza = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField()
    dueño = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mascotas')

    def __str__(self):
        return f"{self.nombre} ({self.especie})"


class ConsultaVeterinaria(models.Model):
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name='consultas')
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()

    def __str__(self):
        return f"Consulta de {self.mascota.nombre} - {self.fecha.strftime('%Y-%m-%d')}"


class Vacuna(models.Model):
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name='vacunas')
    nombre = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.mascota.nombre}"
