from rest_framework import serializers
from cabinet.models import *

class CabinetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cabinet
        fields = "__all__"
        
        
        
    