from django.db import models
from django.contrib.auth.models import User

SCHOOL_LEVEL = [
    ('Primaria', 'Primaria'),
    ('Secundaria', 'Secundaria'),
    ('Técnica y Profesional', 'Técnica y Profesional'),
    ('Medio Superior', 'Medio Superior'),
    ('Superior', 'Superior'),
]

class Parent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, verbose_name="Nombre", null=True)
    last_name = models.CharField(max_length=50, verbose_name="Apellidos", null=True)
    nip = models.CharField(max_length=50, verbose_name="NIP", null=True, unique = True)
    date_birth = models.DateField(verbose_name="Fecha de nacimiento", null=True)
    address = models.CharField(max_length=200, verbose_name="Dirección", null=True)
    phone = models.CharField(max_length=50, verbose_name="Teléfono", null=True)
    school_level = models.CharField(max_length=50, choices=SCHOOL_LEVEL, verbose_name="Nivel escolar", null=True)
    work_center = models.CharField(max_length=1000, verbose_name="Centro de trabajo", null=True)
    position = models.CharField(max_length=1000, verbose_name="Cargo", null=True)
    illnesses = models.CharField(max_length=1000, verbose_name="Enfermedades que padece", null=True)
    alcoholism = models.BooleanField(verbose_name="Alcoholismo", null=True)
    smoking = models.BooleanField(verbose_name="Tabaquismo", null=True)
    is_mother = models.BooleanField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        first_name = self.first_name if self.first_name else ''
        last_name = self.last_name if self.last_name else ''
        return f"{first_name} {last_name}"

    class Meta:
        managed = True
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'