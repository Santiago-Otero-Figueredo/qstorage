from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import FolderVS


router = DefaultRouter()
router.register('folders', FolderVS, basename='folders')


app_name = 'directories'

urlpatterns = [
    path('', include(router.urls)),  
]