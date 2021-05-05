import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_manager = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    firm = models.ForeignKey('firm.Firm', blank=True, null=True, related_name='users', on_delete=models.CASCADE)
    worksite = models.ManyToManyField('firm.Worksite', blank=True, verbose_name='Şantiye')
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(r'^\d{10}$')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ['-id']

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('user:profile_update', kwargs={'pk':self.pk})

    def get_image_or_default(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/site/img/user.png'

    def save(self, *args, **kwargs):
        if self.image:
            self.image.name = slugify(str(self.firm).replace('ı','i'))+'/img/'+self.email.split('@')[0]+os.path.splitext(self.image.name)[1]
        return super(User, self).save(*args, **kwargs)


# BÜTÜN MODELLERİN İŞLEMLERİNİ KAYIT ALTINA ALACAĞIZ. HER MODEL İÇİN SİNYAL (SİGNAL) TANIMLANACAKTIR.
class Logger(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', verbose_name='User', related_name='loggers', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='Tablo Adı')
    row = models.BigIntegerField(verbose_name='Tablo ID')
    data = models.TextField(verbose_name='Veri')
    action = models.CharField(max_length=10, verbose_name='İşlem')  # saved or deleted
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Logger'
        ordering = ['-id']

    def __str__(self):
        return self.name