from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import FolderVS, FileVS


router = DefaultRouter()
router.register('folders', FolderVS, basename='folders')
router.register('files', FileVS, basename='files')


app_name = 'directories'

urlpatterns = [
    path('', include(router.urls)),
]
