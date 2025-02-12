from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PageVisit(models.Model):
    visit_count = models.IntegerField(default=0)
    last_visited = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        # return f"{self.url}: {self.visit_count} visits"
        return self.ip_address
    
    class Meta:
        managed = True
        verbose_name = 'PageVisit'
        verbose_name_plural = 'PageVisits'