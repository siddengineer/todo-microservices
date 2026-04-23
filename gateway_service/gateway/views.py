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


# import requests
# from django.http import JsonResponse
# from concurrent.futures import ThreadPoolExecutor, TimeoutError

# # Docker service name (correct)
# TODO_SERVICE_URL = "http://todo_service:8001"

# # Bulkhead: limit concurrent calls
# executor = ThreadPoolExecutor(max_workers=3)


# def get_todos(request):
#     try:
#         future = executor.submit(
#             requests.get,
#             f"{TODO_SERVICE_URL}/todos/",
#             headers={"Host": "localhost"}   # ✅ IMPORTANT FIX
#         )

#         response = future.result(timeout=2)

#         return JsonResponse(response.json(), safe=False)

#     except TimeoutError:
#         return JsonResponse({"error": "Todo service timeout"}, status=503)

#     except Exception as e:
#         print("ERROR:", e)   # ✅ debug visibility
#         return JsonResponse({"error": "Service unavailable"}, status=503)


# def add_todo(request):
#     try:
#         if request.method == "POST":
#             future = executor.submit(
#                 requests.post,
#                 f"{TODO_SERVICE_URL}/add/",
#                 data=request.POST,
#                 headers={"Host": "localhost"}   # ✅ IMPORTANT FIX
#             )

#             response = future.result(timeout=2)

#             return JsonResponse(response.json(), safe=False)

#     except TimeoutError:
#         return JsonResponse({"error": "Todo service timeout"}, status=503)

#     except Exception as e:
#         print("ERROR:", e)   # ✅ debug visibility
#         return JsonResponse({"error": "Service unavailable"}, status=503)








# import requests
# from django.http import JsonResponse
# from concurrent.futures import ThreadPoolExecutor, TimeoutError

# TODO_SERVICE_URL = "http://todo_service:8001"

# executor = ThreadPoolExecutor(max_workers=3)


# # ✅ Helper: Extract JWT from request/session
# def get_auth_headers(request):
#     token = request.session.get("jwt")  # from SAML login

#     if not token:
#         return None

#     return {
#         "Authorization": f"Bearer {token}",
#         "Host": "localhost"
#     }


# def get_todos(request):
#     try:
#         headers = get_auth_headers(request)

#         if not headers:
#             return JsonResponse({"error": "Unauthorized"}, status=401)

#         future = executor.submit(
#             requests.get,
#             f"{TODO_SERVICE_URL}/todos/",
#             headers=headers
#         )

#         response = future.result(timeout=2)

#         return JsonResponse(response.json(), safe=False)

#     except TimeoutError:
#         return JsonResponse({"error": "Todo service timeout"}, status=503)

#     except Exception as e:
#         print("ERROR:", e)
#         return JsonResponse({"error": "Service unavailable"}, status=503)


# def add_todo(request):
#     try:
#         if request.method == "POST":

#             headers = get_auth_headers(request)

#             if not headers:
#                 return JsonResponse({"error": "Unauthorized"}, status=401)

#             future = executor.submit(
#                 requests.post,
#                 f"{TODO_SERVICE_URL}/add/",
#                 data=request.POST,
#                 headers=headers
#             )

#             response = future.result(timeout=2)

#             return JsonResponse(response.json(), safe=False)

#     except TimeoutError:
#         return JsonResponse({"error": "Todo service timeout"}, status=503)

#     except Exception as e:
#         print("ERROR:", e)
#         return JsonResponse({"error": "Service unavailable"}, status=503)








# import requests
# import jwt
# import datetime
# from django.http import JsonResponse, HttpResponse
# from concurrent.futures import ThreadPoolExecutor, TimeoutError
# from onelogin.saml2.auth import OneLogin_Saml2_Auth

# # =========================
# # CONFIG
# # =========================
# TODO_SERVICE_URL = "http://todo_service:8001"
# SECRET_KEY = "your-secret-key"  # move to settings later

# executor = ThreadPoolExecutor(max_workers=3)


# # =========================
# # SAML AUTH SETUP
# # =========================
# def init_saml_auth(request):
#     return OneLogin_Saml2_Auth(request)


# # =========================
# # SAML LOGIN
# # =========================
# def saml_login(request):
#     auth = init_saml_auth(request)
#     return auth.login()


# # =========================
# # SAML ACS (MAIN LOGIC)
# # =========================
# def saml_acs(request):
#     auth = init_saml_auth(request)
#     auth.process_response()

#     if auth.is_authenticated():
#         user_email = auth.get_nameid()

#         # 🔥 Create JWT
#         payload = {
#             "email": user_email,
#             "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#         }

#         token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

#         # 🔥 Store JWT in session
#         request.session["jwt"] = token

#         return HttpResponse(f"✅ Logged in as {user_email}")

#     return HttpResponse("❌ Login failed")


# # =========================
# # SAML METADATA
# # =========================
# def saml_metadata(request):
#     auth = init_saml_auth(request)
#     metadata = auth.get_settings().get_sp_metadata()
#     return HttpResponse(metadata, content_type='text/xml')


# # =========================
# # HELPER: JWT HEADERS
# # =========================
# def get_auth_headers(request):
#     token = request.session.get("jwt")

#     if not token:
#         return None

#     return {
#         "Authorization": f"Bearer {token}",
#         "Host": "localhost"
#     }


# # =========================
# # TODO SERVICE CALLS
# # =========================
# def get_todos(request):
#     try:
#         headers = get_auth_headers(request)

#         if not headers:
#             return JsonResponse({"error": "Unauthorized"}, status=401)

#         future = executor.submit(
#             requests.get,
#             f"{TODO_SERVICE_URL}/todos/",
#             headers=headers
#         )

#         response = future.result(timeout=2)

#         return JsonResponse(response.json(), safe=False)

#     except TimeoutError:
#         return JsonResponse({"error": "Todo service timeout"}, status=503)

#     except Exception as e:
#         print("ERROR:", e)
#         return JsonResponse({"error": "Service unavailable"}, status=503)


# def add_todo(request):
#     try:
#         if request.method == "POST":

#             headers = get_auth_headers(request)

#             if not headers:
#                 return JsonResponse({"error": "Unauthorized"}, status=401)

#             future = executor.submit(
#                 requests.post,
#                 f"{TODO_SERVICE_URL}/add/",
#                 data=request.POST,
#                 headers=headers
#             )

#             response = future.result(timeout=2)

#             return JsonResponse(response.json(), safe=False)

#     except TimeoutError:
#         return JsonResponse({"error": "Todo service timeout"}, status=503)

#     except Exception as e:
#         print("ERROR:", e)
#         return JsonResponse({"error": "Service unavailable"}, status=503)









import requests
import jwt
import datetime
import os

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from onelogin.saml2.auth import OneLogin_Saml2_Auth


# =========================
# CONFIG
# =========================
TODO_SERVICE_URL = "http://todo_service:8001"
SECRET_KEY = "your-secret-key"

executor = ThreadPoolExecutor(max_workers=3)


# =========================
# SAML AUTH SETUP (FIXED)
# =========================
def init_saml_auth(request):
    req = {
        'http_host': request.META.get('HTTP_HOST'),
        'script_name': request.META.get('PATH_INFO'),
        'server_port': request.META.get('SERVER_PORT'),
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy(),
    }

    # 🔥 IMPORTANT: Correct path to your saml folder
    saml_path = os.path.join(settings.BASE_DIR, 'saml')

    print("SAML PATH:", saml_path)  # debug

    return OneLogin_Saml2_Auth(
        req,
        custom_base_path=saml_path
    )


# =========================
# SAML LOGIN
# =========================
def saml_login(request):
    auth = init_saml_auth(request)
    return HttpResponse(auth.login())


# =========================
# SAML ACS (MAIN LOGIC)
# =========================
def saml_acs(request):
    auth = init_saml_auth(request)
    auth.process_response()

    errors = auth.get_errors()

    if len(errors) == 0 and auth.is_authenticated():
        user_email = auth.get_nameid()

        # 🔥 Create JWT
        payload = {
            "email": user_email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # 🔥 Store JWT in session
        request.session["jwt"] = token

        return HttpResponse(f"✅ Logged in as {user_email}")

    else:
        return HttpResponse(f"❌ Login failed: {errors}")


# =========================
# SAML METADATA
# =========================
def saml_metadata(request):
    auth = init_saml_auth(request)
    metadata = auth.get_settings().get_sp_metadata()
    return HttpResponse(metadata, content_type='text/xml')


# =========================
# HELPER: JWT HEADERS
# =========================
def get_auth_headers(request):
    token = request.session.get("jwt")

    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}",
        "Host": "localhost"
    }


# =========================
# TODO SERVICE CALLS
# =========================
def get_todos(request):
    try:
        headers = get_auth_headers(request)

        if not headers:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        future = executor.submit(
            requests.get,
            f"{TODO_SERVICE_URL}/todos/",
            headers=headers
        )

        response = future.result(timeout=2)

        return JsonResponse(response.json(), safe=False)

    except TimeoutError:
        return JsonResponse({"error": "Todo service timeout"}, status=503)

    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({"error": "Service unavailable"}, status=503)


def add_todo(request):
    try:
        if request.method == "POST":

            headers = get_auth_headers(request)

            if not headers:
                return JsonResponse({"error": "Unauthorized"}, status=401)

            future = executor.submit(
                requests.post,
                f"{TODO_SERVICE_URL}/add/",
                data=request.POST,
                headers=headers
            )

            response = future.result(timeout=2)

            return JsonResponse(response.json(), safe=False)

    except TimeoutError:
        return JsonResponse({"error": "Todo service timeout"}, status=503)

    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({"error": "Service unavailable"}, status=503)