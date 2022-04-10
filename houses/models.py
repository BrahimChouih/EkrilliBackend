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
        extesion = fileName.split('.')[-1]
        name = '%s-%s' % (datetime.now().date(), datetime.now().time())
        return 'houses/%s_%s.%s' % (instance.house.title, name, extesion)
    elif type(instance) == City:
        # extesion = fileName.split('.')[1]
        try:
            City.objects.get(id=instance.id).picture.delete()
        except:
            pass
        extesion = fileName.split('.')[-1]
        name = '%s-%s' % (datetime.now().date(), datetime.now().time())
        return 'Cities/%s_%s.%s' % (instance.name, name, extesion)


class House(models.Model):
    owner = models.ForeignKey(to=Account, null=False, on_delete=models.CASCADE)
    city = models.ForeignKey(to='City', null=False,
                             on_delete=models.DO_NOTHING)

    HOUSE_TYPE_OPTIONS = (
        ('VILLA', 'VILLA'),
        ('APARTMENT', 'APARTMENT'),
    )
    houseType = models.CharField(
        choices=HOUSE_TYPE_OPTIONS, max_length=100, default='VILLA')

    title = models.CharField(max_length=150, null=False)
    description = models.TextField(max_length=2000, default='')
    price_per_day = models.FloatField(default=0.0, null=True)

    location_latitude = models.FloatField(default=0.0, null=True)
    location_longitude = models.FloatField(default=0.0, null=True)
    isAvailable = models.BooleanField(default=True)
    stars = models.FloatField(default=0.0, null=True)
    numReviews = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Houses'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        try:
            images = Picture.objects.filter(house_id=self.id)
            for img in images:
                img.delete()
        except:
            pass
        return super().delete(*args, **kwargs)


class Picture(models.Model):
    picture = models.ImageField(upload_to=uploadImage)
    house = models.ForeignKey(
        to='House', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Pictures'

    def delete(self, *args, **kwargs):
        try:
            self.picture.delete()
        except:
            pass
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.house.title + ' id : ' + str(self.id)


class City(models.Model):
    name = models.CharField(max_length=30, null=False)
    picture = models.ImageField(upload_to=uploadImage, null=True, blank=True)

    class Meta:
        db_table = 'Cities'

    def delete(self, *args, **kwargs):
        try:
            self.picture.delete()
        except:
            pass
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Rating(models.Model):
    offer = models.ForeignKey(to='Offer', on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000, default='')
    stars = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'Rating'

    def __str__(self):
        return self.offer.user.username + " on "+self.offer.house.title

    def save(self, *args, **kwargs):
        self.offer.house.stars += self.stars
        self.offer.house.numReviews += 1
        self.offer.house.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.offer.house.stars -= self.stars
        self.offer.house.numReviews -= 1
        self.offer.house.save()

        super().delete(*args, **kwargs)


class Offer(models.Model):
    house = models.ForeignKey(to=House, null=False,
                              on_delete=models.CASCADE)
    user = models.ForeignKey(to=Account, null=False,
                             on_delete=models.CASCADE)

    STATUS_OPTIONS = (
        ('NEGOTIATE', 'NEGOTIATE'),
        ('DURING', 'DURING'),
        ('WAITING_FOR_ACCEPTE', 'WAITING_FOR_ACCEPTE'),
        ('DONE', 'DONE'),
    )
    status = models.CharField(
        choices=STATUS_OPTIONS, max_length=100, default='NEGOTIATE')
    total_price = models.FloatField(default=0.0, null=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Offers'

    def __str__(self):
        return self.house.title + ': '+self.user.username

    def save(self, *args, **kwargs):
        if self.status=='DURING':
            self.house.isAvailable = False
        elif self.status=='NEGOTIATE' or self.status=='DONE':
            self.house.isAvailable = True
        self.house.save()
        super().save(*args, **kwargs)
