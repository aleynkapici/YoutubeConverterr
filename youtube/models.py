from django.db import models
from PIL import Image 
from django.contrib.auth.models import User
class DownloadTask(models.Model):
    name = models.CharField(max_length=255, unique=True)
    link = models.URLField()
    image=models.ImageField(upload_to='DownloadTask/',blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_downloader')

    def save(self,args,kwargs):
        super().save(args, kwargs)
        if self.image:
            img=Image.open(self.image.path)
            img=img.resize((300,300),Image.LANZOS)
            img.save(self.image.path)
    def __str__(self):
        return self.name

class fileCreation(models.Model):
    name=models.CharField(max_length=255, unique=True)
    link = models.URLField()
    image=models.ImageField(upload_to='fileVideo/',blank=True,null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    errormessage = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True) 
    
    def save(self,args,kwargs):
        super().save(args, kwargs)
        if self.image:
            img=Image.open(self.image.path)
            img=img.resize((300,300),Image.LANZOS)
            img.save(self.image.path)
    def __str__(self):
        return self.name
    
class processdownload(models.Model):
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        session_key = models.CharField(max_length=50, default="Queued")  

        def __str__(self):
            return self.session_key 
    
