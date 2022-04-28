from django.db import models
from houses.models import  House, Offer
from accounts.models import Account
# Create your models here.


class Favorite(models.Model):
    offer = models.ForeignKey(to=Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Favorites'

    def __str__(self):
        return self.user.username +" --> "+ self.offer.house.title
