from django.db import models
from datetime import datetime
from realtors.models import Realtor

class PhotoAlbum(models.Model):
    title = models.CharField(max_length=200, blank=True)
    def default(self):
        return self.photos.filter(default=True).first()

    def __str__(self):
        return self.title

class Photo(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    album = models.ForeignKey(PhotoAlbum, related_name='photos', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.name:
            if self.default:
                self.name = f'{self.album.title} - main'
            else:
                self.name = self.album.title
        super().save(*args, **kwargs)
        
class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    apt_address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    album = models.OneToOneField(PhotoAlbum, related_name='album', on_delete=models.CASCADE, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
