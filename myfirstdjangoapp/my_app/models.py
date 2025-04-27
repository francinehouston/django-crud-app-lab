from django.db import models
from datetime import timedelta

# Create your models here.



class Artist(models.Model):
    name= models.CharField(max_length=100)
    genre= models.CharField(max_length=100)
    bio= models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Album(models.Model):
    title= models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
   
    def __str__(self):
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=100)
    duration = models.DurationField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    audio_file = models.FileField(upload_to='songs/')
   

    def __str__(self):
        return self.title
    
    