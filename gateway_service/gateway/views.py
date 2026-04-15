from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse

TODO_SERVICE_URL = "http://127.0.0.1:8001"

def get_todos(request):
    response = requests.get(f"{TODO_SERVICE_URL}/todos/")
    return JsonResponse(response.json(), safe=False)

def add_todo(request):
    if request.method == "POST":
        response = requests.post(
            f"{TODO_SERVICE_URL}/add/",
            data=request.POST
        )
        return JsonResponse(response.json(), safe=False)