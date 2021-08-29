from django.urls import path
from django.conf.urls import url
from cabinet import views

urlpatterns = [
    path('cabinet/customize/', views.CabinetCustomizeView.as_view()),
]