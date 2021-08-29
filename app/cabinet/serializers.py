# from typing_extensions import Required
# from typing_extensions import Required
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
    
    u_count = serializers.IntegerField(required=False)
    
    
    class Meta(CabinetSerializer.Meta):
        
        fields = CabinetSerializer.Meta.fields
        read_only_fields = ("owner","u_count",)
        
    def create(self, validated_data):
        u_count = validated_data.pop('u_count')
        cabinet = Cabinet.objects.create(**validated_data)
        self.perform_u_creation(instance=cabinet, u_count=u_count)
        return cabinet
    
    def perform_u_creation(self, instance, u_count):
        """
        Creates U's if cabinet is being created
        """
        model = U
        for obj in range(u_count):
            model.objects.create(cabinet=instance, position=obj+1)

    def validate_name(self,value):
        check_query = Cabinet.objects.filter(name=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.pk)
        if self.parent is not None and self.parent.instance is not None:
            cabinet = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=cabinet.pk)
        if check_query.exists():
            raise serializers.ValidationError('Cabinet with such name already exist! Please type different.')
        return value
    
    def validate_u_count(self, value):
        if not value:
            raise serializers.ValidationError('Cabinet needs to have definied u_count to propagate their creation and attach them to the cabinet')
        return value
    


    
class CabinetAccessSerializerExpanded(
    CabinetAccessSerializer, serializers.ModelSerializer
):

    owner = OwnerSerializer()
    

    class Meta(CabinetSerializer.Meta):
        fields = CabinetAccessSerializer.Meta.fields
        read_only_fields = CabinetAccessSerializer.Meta.read_only_fields
