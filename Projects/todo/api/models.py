from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings


class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.username
    

class Task(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False) #hidded to admin as well
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=400)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}_({self.user})"
    

