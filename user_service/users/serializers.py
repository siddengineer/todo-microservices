from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🔥 CUSTOM DATA (token customization)
        token['username'] = user.username
        token['role'] = "user"   # or admin
        token['email'] = user.email

        return token