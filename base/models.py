from django.db import models

# Create your models here.
class Video(models.Model):
    name = models.CharField('Video Name', max_length=50)
    video = models.FileField(upload_to='video')
    caption_file = models.FileField()
    
    def __str__(self):
        return self.name