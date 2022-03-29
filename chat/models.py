from datetime import datetime
from django.db import models
from houses.models import Apartment
from accounts.models import Account
from django.utils import timezone
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
        return self.sender.username + ' with '+self.receiver.username

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if(not self.id):
            self.create_at = timezone.now()
        super().save(*args, **kwargs)
        friends = []
        try:
            user = Friend.objects.get(
                user1=self.sender, user2=self.receiver)
            friends.append(user)
        except:
            pass
        try:
            user = Friend.objects.get(
                user1=self.receiver, user2=self.sender)
            friends.append(user)
        except:
            pass
        # print(not friends[0].last_message.create_at < self.create_at)
        if(len(friends) == 0):
            friend = Friend(user1=self.sender,
                            user2=self.receiver, last_message=self)
            friend.save()
        # and not friends[0].last_message.create_at < self.create_at
        elif friends[0].last_message == None or friends[0].last_message.id != self.id:
            friends[0].last_message = self
            friends[0].save()

        return self

    def delete(self, *args, **kwargs):
        try:
            self.image.delete()
        except:
            pass
        friends = []
        try:
            user = Friend.objects.get(
                user1=self.sender, user2=self.receiver)
            friends.append(user)
        except:
            pass
        try:
            user = Friend.objects.get(
                user1=self.receiver, user2=self.sender)
            friends.append(user)
        except:
            pass
        if(len(friends) != 0):
            friends[0].last_message = None
            friends[0].save()
        return super().delete(*args, **kwargs)


class Friend(models.Model):
    user1 = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name='user1')

    user2 = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name='user2')

    last_message = models.ForeignKey(
        to=Message, on_delete=models.DO_NOTHING, related_name='last_message_last_message', null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user1.username + ' with ' + self.user2.username

    class Meta:
        ordering = ['-created_at']
