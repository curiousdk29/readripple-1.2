from django.db import models
from django.contrib.auth.models import User


from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    age_group = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    file = models.FileField(upload_to='uploaded/')  # Stored in AWS S3
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    def get_view_url(self):
        return self.file.url  # S3 file URL

    def get_download_url(self):
        return self.file.url  # Can use the same, S3 will serve download




class ReadingExercise(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return self.title
