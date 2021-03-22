
from django.urls import path
from django.conf.urls import url
from cabinet import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

app_name = "cabinet"

urlpatterns = [
    url(r'list/', views.CabinetListApiView.as_view(), name = 'cabinet_list'),
    url(r'get/(?P<pk>\d+)/$', views.CabinetRetrieveApiView.as_view(), name = 'cabinet_get'),
    url(r'create/', views.CabinetCreateApiView.as_view(), name = 'cabinet_create'),
    url(r'detail/(?P<pk>\d+)/$', views.CabinetUpdateApiView.as_view(), name = 'cabinet_detail'),
    url(r'delete/(?P<pk>\d+)/$', views.CabinetDeleteApiView.as_view(), name = 'cabinet_delete'),
]
