from django.db import models

from user.models import UserProfile

class UploadedImage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    image_type = models.CharField(max_length=10, choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')])
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

