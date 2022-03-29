from django.db import models
from houses.models import  House
from accounts.models import Account
# Create your models here.


class Favorite(models.Model):
    house = models.ForeignKey(to=House, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Favorites'

    def __str__(self):
        return self.user.username +" --> "+ self.house.title
