# from django.urls import path
# from . import views
# from .views import saml_login, saml_acs

# urlpatterns = [
#     path('todos/', views.get_todos),
#     path('add/', views.add_todo),
#     path('saml/login/', saml_login),
#     path('saml/acs/', saml_acs),
# ]




from django.urls import path
from .views import (
    saml_login,
    saml_acs,
    saml_metadata,
    get_todos,
    add_todo
)

urlpatterns = [
    # 🔐 SAML Routes
    path('saml/login/', saml_login),
    path('saml/acs/', saml_acs),
    path('saml/metadata/', saml_metadata),

    # 📦 API Gateway Routes
    path('todos/', get_todos),
    path('add/', add_todo),
]