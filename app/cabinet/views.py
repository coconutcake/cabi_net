from django.shortcuts import render

from cabinet.models import *
from rest_framework import status
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.response import Response
from cabinet.serializers import *
from drf_yasg.utils import swagger_auto_schema
from django.views.generic import View


class CabinetCustomizeView(View):
    template_name = "cabinet/customize.html"
    
    def get(self, request, *args, **kwargs):
        return render(
            request, 
            self.template_name, 
            self.get_context(request)
            )
    

    def get_context(self, request):
        cabinets = Cabinet.objects.filter(owner=request.user)
        units = U.objects.filter(cabinet__owner=request.user)
        context = {
            "cabinets": cabinets,
            "units": units
        }
        return context



API_COMMENTS = {
    "create": "Tworzy nowy obiekt modelu ",
    "get": "Zwraca instancje obiektu ",
    "get_exp": "Zwraca rozszeżoną instancje obiektu ",
    "list": "Zwraca liste instancji ",
    "put": "Edytuje pola instacji modelu ",
    "delete": "Usuwa instancje obiektu ",
    "patch": "Czesciowo edytuje pola instancji ",
}


# Cabinet ---------------------------------------------------------------------
class CabinetListApiView(generics.ListAPIView):
    model = Cabinet
    serializer_class = CabinetAccessSerializer
    queryset = model.objects.all()

    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("list") + model.__name__,
        operation_summary="",
    )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CabinetRetrieveApiView(generics.RetrieveAPIView):
    model = Cabinet
    serializer_class = CabinetAccessSerializer
    queryset = model.objects.all()

    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("get") + model.__name__,
        operation_summary="",
    )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CabinetRetrieveExpandedApiView(CabinetRetrieveApiView, generics.RetrieveAPIView):

    model = CabinetRetrieveApiView.model
    serializer_class = CabinetAccessSerializerExpanded

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("get_exp") + model.__name__,
        operation_summary="",
    )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CabinetCreateApiView(generics.CreateAPIView):
    model = Cabinet
    responce_serializer = CabinetAccessSerializer
    serializer_class = CabinetAccessSerializer

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("create") + model.__name__,
        operation_summary="",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_create(serializer)
        prepared = self.responce_serializer(created)
        headers = self.get_success_headers(serializer.data)
        return Response(prepared.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    def perform_create(self, serializer):
        """
        Performs object creation and filling owner field 
        with request.user instance
        """
        return serializer.save(owner=self.request.user)
    
    
    def perform_u_creation(self, cabinet, u_count):
        """ 
        Performs u creation according to u_count
        """
        model = U
        for obj in range(u_count):
            model.objects.create(cabi=cabinet, position=obj+1)
        


class CabinetUpdateApiView(generics.UpdateAPIView):
    model = Cabinet
    respose_serializer = CabinetAccessSerializer
    serializer_class = CabinetAccessSerializer
    queryset = model.objects.all()

    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("put") + model.__name__,
        operation_summary="",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("patch") + model.__name__,
        operation_summary="",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CabinetDeleteApiView(generics.DestroyAPIView):
    model = Cabinet
    serializer_class = CabinetAccessSerializer
    queryset = model.objects.all()

    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("delete") + model.__name__,
        operation_summary="",
    )
    def delete(request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# U ---------------------------------------------------------------------------
class UListApiView(generics.ListAPIView):
    model = U
    serializer_class = USerializer
    queryset = model.objects.all()
    
    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(cabinet__owner=self.request.user)
        return queryset

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("list") + model.__name__,
        operation_summary="",
    )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class URetrieveApiView(generics.RetrieveAPIView):
    model = U
    serializer_class = USerializer
    queryset = model.objects.all()

    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(cabinet__owner=self.request.user)
        return queryset

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("get") + model.__name__,
        operation_summary="",
    )
    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UCreateApiView(generics.CreateAPIView):
    model = U
    responce_serializer = USerializer
    serializer_class = USerializer

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("create") + model.__name__,
        operation_summary="",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UUpdateApiView(generics.UpdateAPIView):
    model = U
    respose_serializer = USerializer
    serializer_class = USerializer
    queryset = model.objects.all()
     
    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(cabinet__owner=self.request.user)
        return queryset
    
    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("put") + model.__name__,
        operation_summary="",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("patch") + model.__name__,
        operation_summary="",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UDeleteApiView(generics.DestroyAPIView):
    model = U
    serializer_class = USerializer
    queryset = model.objects.all()
    
    def get_queryset(self):
        """
        Returns only owned cabinets
        """
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(cabinet__owner=self.request.user)
        return queryset

    @swagger_auto_schema(
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("delete") + model.__name__,
        operation_summary="",
    )
    def delete(request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
