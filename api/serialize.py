from rest_framework import serializers
from ToDo.models import TODO

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TODO
        fields = '__all__'