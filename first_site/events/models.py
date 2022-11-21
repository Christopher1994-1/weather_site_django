from django.db import models

# Create your models here.
class SubList(models.Model):
    email = models.EmailField("Email Address")
    
    def __str__(self):
        return self.email
