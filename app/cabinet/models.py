from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import DefaultObject
from django.core.validators import MinValueValidator, MaxValueValidator


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
