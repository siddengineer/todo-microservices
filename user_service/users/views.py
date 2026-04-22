from django.shortcuts import render
from .serializers import CustomTokenSerializer
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer