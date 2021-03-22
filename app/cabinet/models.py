from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from core.models import DefaultObject



class Cabinet(DefaultObject, models.Model):
    """
    Model szafy serwerowej
    """
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("Właściciel szafy"), 
        on_delete=models.CASCADE,
        blank=True
        )   
    
    

    class Meta:
        verbose_name = _("Cabinet")
        verbose_name_plural = _("Cabinets")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Cabinet_detail", kwargs={"pk": self.pk})
