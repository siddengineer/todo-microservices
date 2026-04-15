from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer

@api_view(['GET'])
def get_todos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_todo(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

@api_view(['PUT'])
def update_todo(request, id):
    todo = Todo.objects.get(id=id)
    serializer = TodoSerializer(todo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

@api_view(['DELETE'])
def delete_todo(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return Response({"message": "Deleted"})