from django.db import models
from pgvector.django import VectorField
from django.utils import timezone
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Dodane pole user


    def __str__(self):
        return self.title


class DocumentVector(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    embedding = VectorField(dimensions=384)


