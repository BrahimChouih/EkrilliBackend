from datetime import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


def uploadImage(instance, fileName):
    try:
        Account.objects.get(id=instance.id).picture.delete()
    except:
        print('')
    extesion = fileName.split('.')[1]
    name = '%s-%s' % (datetime.now().date(), datetime.now().time())
    return 'users/%s_pictuer_%s.%s' % (instance.id, name, extesion)



class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    ##################### Contact Info ###################################
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True)
    username = models.CharField(max_length=60, unique=True)
    phone = models.CharField(max_length=20, blank=True)

    ######################### picture ####################################
    picture = models.ImageField(upload_to=uploadImage, null=True, blank=True)

    ########################### personal info ############################
    LANGUAGE_OPTIONS = [
        ('ARABIC', 'ARABIC'),
        ('ENGLISH', 'ENGLISH'),
        ('FRENCH', 'FRENCH'),
    ]

    language = models.CharField(
        choices=LANGUAGE_OPTIONS, max_length=255, default='ARABIC')

    USER_TYPE_OPTIONS = [
        ('OWNER', 'OWNER'),
        ('TENANT', 'TENANT'),
    ]

    user_type = models.CharField(
        choices=USER_TYPE_OPTIONS, max_length=255, default='TENANT')

    location = models.CharField(max_length=100, blank=True, null=True, default='')

    about_me = models.TextField(blank=True, null=True, default='')

    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
