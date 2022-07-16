from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import (logout_view,
                    register_view)


app_name = "auth_user"

urlpatterns = [
    path('api/login/', obtain_auth_token, name='login'),
    path('api/register/', register_view, name='register'),
    path('api/logout/', logout_view, name='logout'),
]
