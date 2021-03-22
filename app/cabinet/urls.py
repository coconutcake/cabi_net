
from django.urls import path
from django.conf.urls import url
from cabinet import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

app_name = "cabinet"

urlpatterns = [
    path('create/', views.CabinetCreateApiView.as_view(), name = 'cabinet_create'),
]
