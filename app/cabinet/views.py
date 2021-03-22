from django.shortcuts import render

from cabinet.models import *
from rest_framework import status
from rest_framework import \
    generics,authentication,permissions
from rest_framework.settings import \
    api_settings
from rest_framework.response import Response  
from cabinet.serializers import *
from drf_yasg.utils import swagger_auto_schema



API_COMMENTS = {
    "create": "Tworzy nowy obiekt modelu ",
    "get": "Zwraca instancje obiektu ",
    "list": "Zwraca liste instancji ",
    "put": "Edytuje pola instacji modelu ",
    "delete": "Usuwa instancje obiektu ",
    "patch": "Czesciowo edytuje pola instancji "
}


class CabinetListApiView(generics.ListAPIView):
    model = Cabinet
    serializer_class = CabinetSerializer
    queryset = model.objects.all()

    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("list") + model.__name__,
        operation_summary = ""
        )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class CabinetRetrieveApiView(generics.RetrieveAPIView):
    model = Cabinet
    serializer_class = CabinetSerializer
    queryset = model.objects.all()
    
    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("get") + model.__name__,
        operation_summary = ""
        )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class CabinetCreateApiView(generics.CreateAPIView):
    model = Cabinet
    responce_serializer = CabinetSerializer
    serializer_class = CabinetAccessSerializer
    
    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("create") + model.__name__,
        operation_summary = ""
        )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_create(serializer)
        prepared = self.responce_serializer(created)
        headers = self.get_success_headers(serializer.data)
        return Response(
            prepared.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
        # return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Performs object creation and filling owner field 
        with request.user instance
        """
        return serializer.save(owner=self.request.user)



class CabinetUpdateApiView(generics.UpdateAPIView):
    model = Cabinet
    respose_serializer = CabinetSerializer
    serializer_class = CabinetAccessSerializer
    queryset = model.objects.all()
    
    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
    
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
    
    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
    
    @swagger_auto_schema(\
        tags = [model.__name__],
        operation_description = API_COMMENTS.get("delete") + model.__name__,
        operation_summary = ""
        ) 
    def delete(request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)