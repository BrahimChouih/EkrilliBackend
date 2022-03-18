from django.db import models
from apartments.models import Apartment
from accounts.models import Account
# Create your models here.


class Favorite(models.Model):
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username +" --> "+ self.apartment.title


class History(models.Model):
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username +" --> "+ self.apartment.title

    class Meta:
        ordering = ['-created_at']
