from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import DefaultObject
from django.core.validators import MinValueValidator, MaxValueValidator



class DeviceType(models.Model):
    """
    Model typu urzadzenia
    """
    

    class Meta:
        verbose_name = _("DeviceType")
        verbose_name_plural = _("DeviceTypes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DeviceType_detail", kwargs={"pk": self.pk})


class Device(models.Model):
    """
    Model urzadzeń
    """
    device_type = models.ForeignKey(
        DeviceType, 
        verbose_name=_("device_type"), 
        on_delete=models.CASCADE
        )
    serial_no = models.CharField(_("50"), max_length=50)

    

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Device_detail", kwargs={"pk": self.pk})


class Port(DefaultObject,models.Model):
    """
    Podel portow
    """
    device = models.ForeignKey(
        Device, 
        verbose_name=_("device"), 
        on_delete=models.CASCADE
        )
    

    class Meta:
        verbose_name = _("Port")
        verbose_name_plural = _("Ports")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Port_detail", kwargs={"pk": self.pk})


class Cabinet(DefaultObject, models.Model):
    """
    Model szafy serwerowej
    """

    owner = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Właściciel szafy"),
        on_delete=models.CASCADE,
        blank=True,
    )

    class Meta:
        verbose_name = _("Cabinet")
        verbose_name_plural = _("Cabinets")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Cabinet_detail", kwargs={"pk": self.pk})


class U(models.Model):
    """
    Model pozycji U szafy serwerowej
    """

    position = models.IntegerField(
        _("pozycja"), validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    cabinet = models.ForeignKey(
        Cabinet,
        verbose_name=_("cabinet"), 
        on_delete=models.CASCADE,
        null=True,
        )

    class Meta:
        verbose_name = _("U")
        verbose_name_plural = _("Us")

    def __str__(self):
        return f"U-{self.position}, C-{self.cabinet}"

    def get_absolute_url(self):
        return reverse("U_detail", kwargs={"pk": self.pk})
    

class UStack(DefaultObject, models.Model):
    """
    Model stacku U
    """
    
    device = models.ForeignKey(
        Device, 
        verbose_name=_("device"), 
        on_delete=models.CASCADE
        )
    u = models.ManyToManyField(U, verbose_name=_("unit"))
    
    class Meta:
        verbose_name = _("UStack")
        verbose_name_plural = _("UStacks")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("UStack_detail", kwargs={"pk": self.pk})