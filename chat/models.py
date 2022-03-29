from datetime import datetime
from django.db import models
from django.utils import timezone
from houses.models import Offer
# Create your models here.


def uploadImage(instance, fileName):
    if type(instance) == Message:
        # extesion = fileName.split('.')[1]
        try:
            Message.objects.get(id=instance.id).image.delete()
        except:
            pass
        extesion = fileName.split('.')[1]
        name = '%s-%s' % (datetime.now().date(), datetime.now().time())
        return 'messages/%s_to_%s_%s.%s' % (instance.sender.username, instance.receiver.username, name, extesion)


class Message(models.Model):
    offer = models.ForeignKey(
        to=Offer, on_delete=models.CASCADE, null=False, blank=False)
    message_type = models.ForeignKey(
        to='MessageType', on_delete=models.DO_NOTHING, null=False, blank=False)

    message_type_options = (
        ('request','request'),
        ('response','response')
    )
    message_type = models.CharField(choices=message_type_options,max_length=100,default='request')


    content_type_options = (
        ('message','message'),
        ('image','image'),
    )
    content_type = models.CharField(choices=content_type_options,max_length=100,default='message')

    message = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to=uploadImage, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.offer.house.title + ': '+self.offer.tenant.username

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if(not self.id):
            self.create_at = timezone.now()
        super().save(*args, **kwargs)
        return self

    def delete(self, *args, **kwargs):
        try:
            self.image.delete()
        except:
            pass
        return super().delete(*args, **kwargs)


