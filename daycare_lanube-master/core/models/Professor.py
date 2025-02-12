from django.db import models
from django.contrib.auth.models import User

SEX = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
]

SCHOOL_LEVEL = [
    ('Primaria', 'Primaria'),
    ('Secundaria', 'Secundaria'),
    ('Técnica y Profesional', 'Técnica y Profesional'),
    ('Medio Superior', 'Medio Superior'),
    ('Superior', 'Superior'),
]

class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    nip = models.CharField(max_length=50, verbose_name="NIP", null = True, unique = True)
    date_birth = models.DateField(verbose_name="Fecha de nacimiento", null = True)
    address = models.CharField(max_length=200, verbose_name="Dirección", null = True)
    phone = models.CharField(max_length=50, verbose_name="Teléfono", null = True)
    school_level = models.CharField(max_length=50, choices=SCHOOL_LEVEL, verbose_name="Nivel escolar", null = True)
    cv = models.TextField(null = True)
    image = models.ImageField(upload_to='child_images/', blank=True, null=True)
    sex = models.CharField(max_length=50, choices=SEX, null = True)
    active = models.BooleanField(default=True)
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        managed = True
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'