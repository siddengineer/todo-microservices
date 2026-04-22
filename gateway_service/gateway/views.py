# from django.shortcuts import render

# # Create your views here.
# import requests
# from django.http import JsonResponse

# TODO_SERVICE_URL = "http://127.0.0.1:8001"

# def get_todos(request):
#     response = requests.get(f"{TODO_SERVICE_URL}/todos/")
#     return JsonResponse(response.json(), safe=False)

# def add_todo(request):
#     if request.method == "POST":
#         response = requests.post(
#             f"{TODO_SERVICE_URL}/add/",
#             data=request.POST
#         )
#         return JsonResponse(response.json(), safe=False)


import requests
from django.http import JsonResponse
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Docker service name (correct)
TODO_SERVICE_URL = "http://todo_service:8001"

# Bulkhead: limit concurrent calls
executor = ThreadPoolExecutor(max_workers=3)


def get_todos(request):
    try:
        future = executor.submit(
            requests.get,
            f"{TODO_SERVICE_URL}/todos/",
            headers={"Host": "localhost"}   # ✅ IMPORTANT FIX
        )

        response = future.result(timeout=2)

        return JsonResponse(response.json(), safe=False)

    except TimeoutError:
        return JsonResponse({"error": "Todo service timeout"}, status=503)

    except Exception as e:
        print("ERROR:", e)   # ✅ debug visibility
        return JsonResponse({"error": "Service unavailable"}, status=503)


def add_todo(request):
    try:
        if request.method == "POST":
            future = executor.submit(
                requests.post,
                f"{TODO_SERVICE_URL}/add/",
                data=request.POST,
                headers={"Host": "localhost"}   # ✅ IMPORTANT FIX
            )

            response = future.result(timeout=2)

            return JsonResponse(response.json(), safe=False)

    except TimeoutError:
        return JsonResponse({"error": "Todo service timeout"}, status=503)

    except Exception as e:
        print("ERROR:", e)   # ✅ debug visibility
        return JsonResponse({"error": "Service unavailable"}, status=503)