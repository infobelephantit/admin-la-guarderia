from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models.Professor import Professor
from core.models.Parent import Parent

ROLES = [
    ('Admin', 'Admin'),
    ('Profesor', 'Profesor'),
    ('Progenitor', 'Progenitor'),
    ('Supervisor', 'Supervisor'),
]

class UserApp(User):
    rol = models.CharField(max_length=20, choices=ROLES, default='Admin')
    nip = models.CharField(max_length=20,unique = True)
    mother = models.BooleanField(default = True)       
    terms = models.BooleanField(default = False) 

    class Meta:
        managed = True
        verbose_name = 'UserApp'
        verbose_name_plural = 'UsersApp'

@receiver(post_save, sender=UserApp, dispatch_uid="save_parent_professor")
def save_parent_professor(sender, instance, **kwargs):
    try:
        if instance.rol == "Progenitor":
            instance.groups.add(Group.objects.get(name="Progenitor"))
            if not Parent.objects.filter(nip = instance.nip).exists():
                parent = Parent()
                parent.user = instance
                parent.nip = instance.nip
                parent.is_mother = True if instance.mother else False
                parent.save()
            else:
                parent = Parent.objects.get(nip = instance.nip)
                parent.user = instance
                parent.save()                            
        elif instance.rol == "Profesor":
            instance.groups.add(Group.objects.get(name="Profesor"))
            professor = Professor()
            professor.user = instance
            professor.nip = instance.nip
            professor.save()
        elif instance.rol == "Admin":
            instance.is_staff = True
            instance.groups.add(Group.objects.get(name="Admin"))
            instance.save()
        elif instance.rol == "Supervisor":
            instance.groups.add(Group.objects.get(name="Supervisor"))
            professor = Professor()
            professor.user = instance
            professor.nip = instance.nip
            professor.is_supervisor = True
            professor.save()
    except:
        pass