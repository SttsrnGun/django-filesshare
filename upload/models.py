import os.path
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Upload(models.Model):
    file = models.FileField(upload_to="upload")
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    max_downloads = models.IntegerField()
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return str(self.file)
        
    def delete(self):
        self.is_delete = True
        # https://stackoverflow.com/questions/33080360/how-to-delete-files-from-filesystem-using-post-delete-django-1-8
        if os.path.isfile(self.file.path):
            os.remove(self.file.path) 
            
        return self.save()
    
    def get_absolute_url(self):
        return reverse("detail", args=(self.id,))
    
    def perform_download(self, password=None):
        if self.max_downloads < 1:
            raise FieldDoesNotExist("download limit exceeded")
        
        if timezone.now() > self.expired_at:
            raise FieldDoesNotExist("the file has been expired")
        
        if password and ( not check_password(password, self.password) ):
            raise ValidationError("invalid password")
        
        self.max_downloads -= 1
        self.save()

