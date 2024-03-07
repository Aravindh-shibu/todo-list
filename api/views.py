from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import UserSerializer,TodoSerializers
from rest_framework.viewsets import ViewSet
from rest_framework import authentication,permissions,serializers

from todoapp.models import Todos

class Registerview(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class TodosView(ViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self,request,*args,**kwargs):
        serializer=TodoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        


    def list(self,request,*args,**kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializers(qs,many=True)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        if todo_object.user!=request.user:
            raise serializers.ValidationError("delete request denied")
        else:
            todo_object.delete()
            return Response(data={"messsage":"deleted successfully"})


    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        