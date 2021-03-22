from django.shortcuts import render

from cabinet.models import *

from rest_framework import \
    generics,authentication,permissions
from rest_framework.settings import \
    api_settings
    
from cabinet.serializers import *
from drf_yasg.utils import swagger_auto_schema



API_COMMENTS = {
    "create": "Tworzy nowy obiekt modelu ",
    "get": "Zwraca instancje obiektu ",
    "put": "Edytuje pola instacji modelu ",
    "delete": "Usuwa instancje obiektu ",
    "patch": "Czesciowo edytuje pola instancji "
}




class CabinetCreateApiView(generics.CreateAPIView):
    model = Cabinet
    serializer_class = CabinetSerializer
    
    
    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("create") + model.__name__,
        operation_summary = ""
        )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    