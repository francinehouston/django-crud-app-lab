from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Artist(models.Model):
    name= models.CharField(max_length=100)
    genre= models.CharField(max_length=100, default='Unknown')
    bio= models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artists',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Album(models.Model):
    title= models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f"{self.title} by {self.artist.name}"

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    duration = models.DurationField()
    audio_file = models.FileField(upload_to='songs/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return self.title
    
    