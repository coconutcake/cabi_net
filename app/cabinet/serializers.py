from rest_framework import serializers
from cabinet.models import *
from django.contrib.auth import get_user_model


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ("password",)


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = "__all__"


class USerializer(serializers.ModelSerializer):
    class Meta:
        model = U
        fields = "__all__"


class CabinetAccessSerializer(CabinetSerializer, serializers.ModelSerializer):
    class Meta(CabinetSerializer.Meta):
        fields = CabinetSerializer.Meta.fields
        read_only_fields = ("owner",)


class CabinetAccessSerializerExpanded(
    CabinetAccessSerializer, serializers.ModelSerializer
):

    owner = OwnerSerializer()

    class Meta(CabinetSerializer.Meta):
        fields = CabinetAccessSerializer.Meta.fields
        read_only_fields = CabinetAccessSerializer.Meta.read_only_fields
