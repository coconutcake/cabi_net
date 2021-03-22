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


class CabinetRetrieveApiView(generics.RetrieveAPIView):
    model = Cabinet
    serializer_class = CabinetSerializer
    queryset = model.objects.all()
    
    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("get") + model.__name__,
        operation_summary = ""
        )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

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
    
    
class CabinetUpdateApiView(generics.UpdateAPIView):
    model = Cabinet
    serializer_class = CabinetSerializer
    queryset = model.objects.all()
    
    
    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("put") + model.__name__,
        operation_summary = ""
        )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    
    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("patch") + model.__name__,
        operation_summary = ""
        )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CabinetDeleteApiView(generics.DestroyAPIView):
    model = Cabinet
    serializer_class = CabinetSerializer
    queryset = model.objects.all()
    
    
    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("delete") + model.__name__,
        operation_summary = ""
        ) 
    def delete(request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)