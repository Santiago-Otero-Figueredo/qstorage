from functools import partial
from traceback import print_tb
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


    @action(detail=False, methods=['patch'], url_path='move-files',
            url_name='move-files', permission_classes=[IsAuthenticatedOwnerFolderFileUser])
    def move_files(self, request):
        id_new_parent_folder = self.request.data.get('parent_folder', None)
        list_of_ids_to_move = self.request.data.get('files_to_move', None)

        if id_new_parent_folder is None:
            return Response(
                {'message': 'The parent_folder field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if list_of_ids_to_move is None or len(list_of_ids_to_move) == 0:
            return Response(
                {'message': 'The list_of_ids_to_move field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        files_to_move = list(map(int, list_of_ids_to_move))
        new_parent_folder = self.request.user.get_folder_by_id(id_new_parent_folder)

        if new_parent_folder is None:
            return Response(
                {'message': 'The destination folder does not exists. Check it and try again'},
                status=status.HTTP_404_NOT_FOUND
            )

        if File.get_all_files_by_user_and_list_ids(self.request.user, files_to_move).count() != len(files_to_move):
            return Response(
                {'message': 'You do not have the right permissions to move the folders'},
                status=status.HTTP_403_FORBIDDEN
            )

        if new_parent_folder.pk in File.get_all_pk_parent_folder_list_ids_files(files_to_move):
            return Response(
                {'message': 'The new folder to be moved to must be different than current parent folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        if File.get_all_files_names_by_user_and_list_ids(self.request.user, files_to_move) & new_parent_folder.get_all_files_name():
            return Response(
                {'message': 'The new folder to be moved to must be different name of the children folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        if File.move_many_files_into_another_folder(files_to_move, new_parent_folder) is True:
            return Response(
                {'message': 'Files moved successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'An error occurred while moving the folder.'},
                status=status.HTTP_400_BAD_REQUEST
            )
