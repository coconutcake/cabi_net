from rest_framework import serializers
from cabinet.models import *

class CabinetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cabinet
        fields = "__all__"

class CabinetAccessSerializer(CabinetSerializer, serializers.ModelSerializer):

    class Meta(CabinetSerializer.Meta):
        fields = CabinetSerializer.Meta.fields
        read_only_fields = ("owner",)





