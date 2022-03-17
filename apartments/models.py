from datetime import datetime
from xml.etree.ElementTree import Comment
from django.db import models
from accounts.models import Account

# Create your models here.


def uploadImage(instance, fileName):
    if type(instance) == Picture:
        # extesion = fileName.split('.')[1]
        try:
            Picture.objects.get(id=instance.id).picture.delete()
        except:
            pass
        extesion = fileName.split('.')[1]
        name = '%s-%s' % (datetime.now().date(), datetime.now().time())
        return 'gig/%s_%s.%s' % (instance.apartment.title, name, extesion)
    elif type(instance) == City:
        # extesion = fileName.split('.')[1]
        try:
            City.objects.get(id=instance.id).picture.delete()
        except:
            pass
        extesion = fileName.split('.')[1]
        name = '%s-%s' % (datetime.now().date(), datetime.now().time())
        return 'Cities/%s_%s.%s' % (instance.name, name, extesion)


class Apartment(models.Model):
    title = models.CharField(max_length=150, null=False)
    owner = models.ForeignKey(to=Account, null=False, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, default='')
    price_per_day = models.FloatField(default=0.0, null=True)
    city = models.ForeignKey(to='City', null=False,
                             on_delete=models.DO_NOTHING)
    location_latitude = models.FloatField(default=0.0, null=True)
    location_longitude = models.FloatField(default=0.0, null=True)
    isAvailable = models.BooleanField(default=True)
    stars = models.FloatField(default=0.0, null=True)
    numRaters = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titel


class Picture(models.Model):
    picture = models.ImageField(upload_to=uploadImage)
    apartment = models.ForeignKey(
        to='Apartment', null=False, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        try:
            self.image.delete()
        except:
            pass
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.apartment.title + ' id : ' + str(self.id)


class City(models.Model):
    name = models.CharField(max_length=30, null=False)
    picture = models.ImageField(upload_to=uploadImage, null=True, blank=True)

    def delete(self, *args, **kwargs):
        try:
            self.picture.delete()
        except:
            pass
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Rate(models.Model):
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000, default='')
    stars = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['-created_at']
