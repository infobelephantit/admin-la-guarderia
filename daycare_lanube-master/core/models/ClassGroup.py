from django.db import models
from django.contrib.auth.models import User
from .Child import Child

class ClassGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre", unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    childs = models.ManyToManyField(Child,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ClassGroup'
        verbose_name_plural = 'ClassGroups'