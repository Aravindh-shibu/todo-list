from rest_framework import serializers
from django.contrib.auth.models import User
from todoapp.models import Todos
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username","email","password")

    def create(self,validated_data):
     return User.objects.create_user(**validated_data)       

class TodoSerializers(serializers.ModelSerializer):
   user=serializers.StringRelatedField()
   class Meta:
      model=Todos
      fields="__all__"
      read_only_fields=("id","status","user")