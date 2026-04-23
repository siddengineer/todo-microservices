# from django.shortcuts import render
# from .serializers import CustomTokenSerializer
# # Create your views here.
# from rest_framework_simplejwt.views import TokenObtainPairView

# class LoginView(TokenObtainPairView):
#     serializer_class = CustomTokenSerializer




from django.http import JsonResponse
import jwt

SECRET = "mysecretkey"


# ✅ Common JWT verification
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


# ✅ Example: Get logged-in user info
def get_user_profile(request):
    user = verify_token(request)

    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    return JsonResponse({
        "message": "User profile fetched",
        "user": user
    })