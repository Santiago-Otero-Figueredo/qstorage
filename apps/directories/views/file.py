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
        list_of_ids_to_move = self.request.data.getlist('files_to_move', None)

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

    @action(detail=False, methods=['patch'], url_path='move-to-recycle-bin',
            url_name='move-to-recycle-bin', permission_classes=[IsAuthenticatedOwnerFolderFileUser])
    def move_to_recycle_bin(self, request):
        """ move files to the recycle bin and prepare for his elimination """
        data = dict(request.data)
        list_of_ids_to_move = data.get('files_to_disable', None)
        try:

            if list_of_ids_to_move is None or len(list_of_ids_to_move) == 0:
                return Response(
                    {'message': 'The files_to_disable field is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            files_to_disable = list(map(int, list_of_ids_to_move))

            if File.get_all_files_by_user_and_list_ids(self.request.user, files_to_disable).count() != len(files_to_disable):
                return Response(
                    {'message': 'You do not have the right permissions to move the files'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if File.disabled_many_files(files_to_disable) is True:
                return Response(
                    {'message': 'Files moved to recycle bin. Will be delete in 3 days'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'An error occurred while moving the files.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='recover-files',
            url_name='recover-files', permission_classes=[IsAuthenticatedOwnerFolderFileUser])
    def recover_folder(self, request):
        """ recover files from the recycle bin """
        data = dict(request.data)
        list_of_ids_to_move = data.get('files_to_recover', None)

        try:

            if list_of_ids_to_move is None or len(list_of_ids_to_move) == 0:
                return Response(
                    {'message': 'The files_to_recover field is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            files_to_recover = list(map(int, list_of_ids_to_move))

            if File.get_all_files_by_user_and_list_ids(self.request.user, files_to_recover).count() != len(files_to_recover):
                return Response(
                    {'message': 'You do not have the right permissions to move the files'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if File.recover_many_files(files_to_recover) is True:
                return Response(
                    {'message': 'Files arecover successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'An error occurred while moving the files.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-file',
            url_name='delete-file', permission_classes=[IsAuthenticatedOwnerFolderFileUser])
    def delete_folder(self, request):
        """ Delete the folder and his children folder with all the content """
        data = dict(request.data)
        list_of_ids_to_delete = data.get('files_to_delete', None)

        try:
            if list_of_ids_to_delete is None or len(list_of_ids_to_delete) == 0:
                return Response(
                    {'message': 'The files_to_delete field is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            files_to_delete = list(map(int, list_of_ids_to_delete))

            if File.get_all_files_by_user_and_list_ids(self.request.user, files_to_delete).count() != len(files_to_delete):
                return Response(
                    {'message': 'You do not have the right permissions to delete the files'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if File.delete_many_files(files_to_delete) is True:
                return Response(
                    {'message': 'Files deleted successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )

            else:
                return Response(
                    {'message': 'An error occurred while deleting the files.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)
