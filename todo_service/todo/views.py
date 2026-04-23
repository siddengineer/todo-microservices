# from django.shortcuts import render

# # Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Todo
# from .serializers import TodoSerializer

# @api_view(['GET'])
# def get_todos(request):
#     todos = Todo.objects.all()
#     serializer = TodoSerializer(todos, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def add_todo(request):
#     serializer = TodoSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)

# @api_view(['PUT'])
# def update_todo(request, id):
#     todo = Todo.objects.get(id=id)
#     serializer = TodoSerializer(todo, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)

# @api_view(['DELETE'])
# def delete_todo(request, id):
#     todo = Todo.objects.get(id=id)
#     todo.delete()
#     return Response({"message": "Deleted"})








from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
import jwt

# 🔐 SAME SECRET as gateway
SECRET = "mysecretkey"


# ✅ JWT Verification Function
def verify_token(request):
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        token = auth_header.split()[1]
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])

        return decoded

    except Exception as e:
        print("JWT ERROR:", e)
        return None


# ✅ GET TODOS (Protected)
@api_view(['GET'])
def get_todos(request):
    user = verify_token(request)

    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)


# ✅ ADD TODO (Protected)
@api_view(['POST'])
def add_todo(request):
    user = verify_token(request)

    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)


# ✅ UPDATE TODO (Protected)
@api_view(['PUT'])
def update_todo(request, id):
    user = verify_token(request)

    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    todo = Todo.objects.get(id=id)
    serializer = TodoSerializer(todo, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)


# ✅ DELETE TODO (Protected)
@api_view(['DELETE'])
def delete_todo(request, id):
    user = verify_token(request)

    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    todo = Todo.objects.get(id=id)
    todo.delete()
    return Response({"message": "Deleted"})