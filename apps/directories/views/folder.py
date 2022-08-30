from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.directories.models import Folder

from ..serializers import FolderCreateSerializer
from ..permissions import IsAuthenticatedOwnerFolderUser


class FolderVS(ModelViewSet):

    serializer_class = FolderCreateSerializer
    permission_classes = [IsAuthenticatedOwnerFolderUser]
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_queryset(self):
        return self.request.user.own_entity_directories.all()

    @action(detail=True, methods=['post'], url_path='create-folder',
            url_name='create-folder', permission_classes=[IsAuthenticatedOwnerFolderUser])
    def create_new_folder(self, request, pk):
        """ Create a new folder inside another using the pk to get the parent folder"""

        parent_folder = self.get_object()

        serializer = FolderCreateSerializer(
            instance=parent_folder,
            data=request.data,
            context={'method': self.request.method, 'owner_user': self.request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='children-folders',
            url_name='children-folders', permission_classes=[IsAuthenticatedOwnerFolderUser])
    def list_children_folders(self, request, pk):
        """ List the children folders of the folder parent"""

        parent_folder = self.get_object()

        serializer = FolderCreateSerializer(parent_folder.get_children(), many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='move-folder',
            url_name='move-folder', permission_classes=[IsAuthenticatedOwnerFolderUser])
    def move_folder(self, request):
        """ Move the folder content to another folder """
        from iteration_utilities import duplicates, unique_everseen

        data = dict(request.data)

        list_of_ids_to_move = data.get('folders_to_move', None)

        id_new_parent_folder = request.POST.get('new_parent_folder', None)

        if id_new_parent_folder is None:
            return Response(
                {'message': 'The new_parent_folder field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if list_of_ids_to_move is None or len(list_of_ids_to_move) == 0:
            return Response(
                {'message': 'The folders_to_move field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        folders_to_move = list(map(int, list_of_ids_to_move))
        new_parent_folder = self.request.user.get_folder_by_id(id_new_parent_folder)

        if new_parent_folder is None:
            return Response(
                {'message': 'The destination folder does not exists. Check it and try again'},
                status=status.HTTP_404_NOT_FOUND
            )

        if self.request.user.get_all_folders_by_list_ids(folders_to_move).count() != len(folders_to_move):
            return Response(
                {'message': 'You do not have the right permissions to move the folders'},
                status=status.HTTP_403_FORBIDDEN
            )

        if new_parent_folder.pk in Folder.get_all_pk_parents_in_list_ids(folders_to_move):
            return Response(
                {'message': 'The new folder to be moved to must be different than current parent folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        if new_parent_folder.pk in folders_to_move:
            return Response(
                {'message': 'The new folder to be moved to must be different than current folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        if self.request.user.get_all_names_of_folders_by_list_ids(folders_to_move) & new_parent_folder.get_children_folder():
            return Response(
                {'message': 'The new folder to be moved to must be different name of the children folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        # Compare the names of the files in the actual folder parent with the new folder parent and avoid move files with same names
        list_names = Folder.get_all_name_files_in_folder_group(folders_to_move)
        duplicated_names = list(unique_everseen(duplicates(list_names)))

        if len(duplicated_names) > 0:
            return Response(
                {'message': 'There are files with the same name in the group of folder to move.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_parent_folder.get_all_files_name() & set(list_names):
            return Response(
                {'message': 'There are files with the same name in the new parent folder to move.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Folder.move_many_folder_into_another(folders_to_move, new_parent_folder) is True:
            return Response(
                {'message': 'Folder moved successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'An error occurred while moving the folder.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['patch'], url_path='move-to-recycle-bin',
            url_name='move-to-recycle-bin', permission_classes=[IsAuthenticatedOwnerFolderUser])
    def move_to_recycle_bin(self, request):
        """ move folders to the recycle bin and prepare for his elimination """

        data = dict(request.data)
        list_of_ids_to_disable = data.get('folders_to_disable', None)
        try:

            if list_of_ids_to_disable is None or len(list_of_ids_to_disable) == 0:
                return Response(
                    {'message': 'The folders_to_disable field is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            folders_to_disable = list(map(int, list_of_ids_to_disable))

            if self.request.user.get_all_folders_by_list_ids(folders_to_disable).count() != len(folders_to_disable):
                return Response(
                    {'message': 'You do not have the right permissions to move the folders'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if Folder.disabled_many_folder_and_children(folders_to_disable) is True:
                return Response(
                    {'message': 'Folder and children moved to recycle bin. Will be delete in 3 days'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'An error occurred while moving the folder.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='recover-folder',
            url_name='recover-folder', permission_classes=[IsAuthenticatedOwnerFolderUser])
    def recover_folder(self, request):
        """ move folders to the recycle bin and prepare for his elimination """
        data = dict(request.data)
        list_of_ids_to_recover = data.get('folders_to_recover', None)

        try:

            if list_of_ids_to_recover is None or len(list_of_ids_to_recover) == 0:
                return Response(
                    {'message': 'The folders_to_recover field is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            folders_to_recover = list(map(int, list_of_ids_to_recover))

            if self.request.user.get_all_folders_by_list_ids(folders_to_recover).count() != len(folders_to_recover):
                return Response(
                    {'message': 'You do not have the right permissions to move the folders'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if Folder.recover_many_folder_and_children(folders_to_recover) is True:
                return Response(
                    {'message': 'Folder and children recover successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'An error occurred while moving the folder.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-folder',
            url_name='delete-folder', permission_classes=[IsAuthenticatedOwnerFolderUser])
    def delete_folder(self, request):
        """ Delete the folder and his children folder with all the content """
        data = dict(request.data)
        list_of_ids_to_delete = data.get('folders_to_delete', None)

        try:
            if list_of_ids_to_delete is None or len(list_of_ids_to_delete) == 0:
                return Response(
                    {'message': 'The folders_to_delete field is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            folders_to_delete = list(map(int, list_of_ids_to_delete))

            if Folder.get_root_folder_by_user(self.request.user).pk in folders_to_delete:
                return Response(
                    {'message': 'You do not have the right permissions to delete the root folder'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if self.request.user.get_all_folders_by_list_ids(folders_to_delete).count() != len(folders_to_delete):
                return Response(
                    {'message': 'You do not have the right permissions to delete the folders'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if Folder.delete_many_folder_and_children(folders_to_delete) is True:
                return Response(
                    {'message': 'Folder and children deleted successfully'},
                    status=status.HTTP_204_NO_CONTENT
                )

            else:
                return Response(
                    {'message': 'An error occurred while deleting the folder.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)
