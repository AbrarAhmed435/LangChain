from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
class Document(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    name=models.CharField(max_length=255)
    file = models.FileField(upload_to="pdfs/",null=True,blank=True) 
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user})"


class YoutubeVideo(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="youtube_videos" #now we can do "user.youtube_videos.all()""
        )
    name=models.CharField(max_length=200)
    url=models.URLField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)


    
class DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk {self.id}"
    

    