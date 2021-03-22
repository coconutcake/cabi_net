from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
from django.utils.translation import ugettext_lazy as _

class DefaultObject(models.Model):
    """
    Klasa obiektu deafultowego
    """
    
    name = models.CharField(_("Nazwa"), max_length=70)
    description = models.TextField(_("Opis"), blank = True)
    

    class Meta:
        verbose_name = _("DefaultObject")
        verbose_name_plural = _("DefaultObjects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DefaultObject_detail", kwargs={"pk": self.pk})


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """ Tworzy uzytkownika """
        if not email:
            raise ValueError('Uzytkownik musi mieć email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password):
        """ Tworzy superusera """
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def create_staff(self,email,password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

