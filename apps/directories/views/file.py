from functools import partial
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.directories.models import Folder

from ..models import File
from ..serializers import FileSerializer
from ..permissions import IsAuthenticatedOwnerFolderFileUser

class FileVS(ModelViewSet):

    serializer_class = FileSerializer
    permission_classes = [IsAuthenticatedOwnerFolderFileUser]
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_queryset(self):
        return File.get_all_files_by_user(self.request.user)

    # def partial_update(self, request, *args, **kwargs):

    #     print("#############----")

    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         print(serializer.data)
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], url_path='list-files',
            url_name='list-files', permission_classes=[IsAuthenticatedOwnerFolderFileUser])
    def list_children_folders(self, request):
        """ List the children folders of the folder parent"""

        parent_folder_id = self.request.data.get('parent_folder', None)
        if parent_folder_id is None:
            return Response(
                {'message': 'The parent_folder field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        parent_folder = Folder.get_by_id(parent_folder_id)
        serializer = FileSerializer(parent_folder.get_all_files(), many=True)

        return Response(serializer.data)

