from django.urls import path
from django.conf.urls import url
from cabinet import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

app_name = "cabinet"

urlpatterns = [
    # Cabinet -----------------------------------------------------------------
    url(r"cabinet/list/", views.CabinetListApiView.as_view(), name="cabinet_list"),
    url(
        r"cabinet/get/(?P<pk>\d+)/$",
        views.CabinetRetrieveApiView.as_view(),
        name="cabinet_get",
    ),
    url(
        r"cabinet/get_exp/(?P<pk>\d+)/$",
        views.CabinetRetrieveExpandedApiView.as_view(),
        name="cabinet_get_exp",
    ),
    url(
        r"cabinet/create/", views.CabinetCreateApiView.as_view(), name="cabinet_create"
    ),
    url(
        r"cabinet/detail/(?P<pk>\d+)/$",
        views.CabinetUpdateApiView.as_view(),
        name="cabinet_detail",
    ),
    url(
        r"cabinet/delete/(?P<pk>\d+)/$",
        views.CabinetDeleteApiView.as_view(),
        name="cabinet_delete",
    ),
    # U -----------------------------------------------------------------------
    url(r"u/list/", views.UListApiView.as_view(), name="u_list"),
    url(r"u/get/(?P<pk>\d+)/$", views.URetrieveApiView.as_view(), name="u_get"),
    url(r"u/create/", views.UCreateApiView.as_view(), name="u_create"),
    url(r"u/detail/(?P<pk>\d+)/$", views.UUpdateApiView.as_view(), name="u_detail"),
    url(r"u/delete/(?P<pk>\d+)/$", views.UDeleteApiView.as_view(), name="u_delete"),
]
