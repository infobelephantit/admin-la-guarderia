from django.db import models
from django.contrib.auth.models import User
from .Child import Child

CURRENCY = [
    ('USD', 'USD'),
    ('Euro', 'Euro'),
]

MONTHS = [
    ('Enero', 'Enero'),
    ('Febrero', 'Febrero'),
    ('Marzo', 'Marzo'),
    ('Abril', 'Abril'),
    ('Mayo', 'Mayo'),
    ('Junio', 'Junio'),
    ('Julio', 'Julio'),
    ('Agosto', 'Agosto'),
    ('Septiembre', 'Septiembre'),
    ('Octubre', 'Octubre'),
    ('Noviembre', 'Noviembre'),
    ('Diciembre', 'Diciembre'),
]

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    paid = models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name = "Niño/a") # Parent paid
    date = models.DateField()
    month = models.CharField(max_length=50, choices=MONTHS, verbose_name = "Mes")
    currency = models.CharField(max_length=50, choices=CURRENCY, verbose_name = "Moneda", default="USD")
    amount = models.FloatField()
    active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.paid} ({self.month})"

    class Meta:
        managed = True
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'
        unique_together = (("paid", "month"),)