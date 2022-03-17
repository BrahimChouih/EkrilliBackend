from datetime import datetime
from email import message
from django.db import models
from apartments.models import Apartment
from accounts.models import Account
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
    sender = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name='receiver')
    apartment = models.ForeignKey(
        to=Apartment, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to=uploadImage, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.apartment.title

    class Meta:
        ordering = ['-created_at']


class Friend(models.Model):
    user1 = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name='first_user')

    user2 = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name='second_user')

    last_message = models.ForeignKey(
        to=Message, on_delete=models.DO_NOTHING, related_name='last_message_last_message', null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.first_user.username + ' with ' + self.second_user.username

    class Meta:
        ordering = ['-created_at']
