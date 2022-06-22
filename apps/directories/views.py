from multiprocessing import context
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Folder
from .serializers import FolderCreateSerializer

from django.shortcuts import render

# Create your views here.

class FolderVS(ModelViewSet):

    serializer_class = FolderCreateSerializer
    queryset = Folder.get_all()
    permission_classes = (IsAuthenticated,)
    

    
    @action(detail=True, methods=('post', ), url_path='create-folder', url_name='create-folder')
    def create_new_folder(self, request, pk):
        
        parent_folder = Folder.get_by_id(pk)
        serializer = FolderCreateSerializer(instance=parent_folder, data=request.data, context={'method':self.request.method})

        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
