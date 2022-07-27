from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.directories.models import Folder

from .serializers import FolderCreateSerializer
from .permissions import IsAuthenticatedOwnerUser
from .utils.folder_manager import FolderManager


class FolderVS(ModelViewSet):

    serializer_class = FolderCreateSerializer
    permission_classes = [IsAuthenticatedOwnerUser]
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_queryset(self):
        return self.request.user.own_entity_directories.all()

    @action(detail=True, methods=['post'], url_path='create-folder',
            url_name='create-folder', permission_classes=[IsAuthenticatedOwnerUser])
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
            url_name='children-folders', permission_classes=[IsAuthenticatedOwnerUser])
    def list_children_folders(self, request, pk):
        """ List the children folders of the folder parent"""

        parent_folder = self.get_object()

        serializer = FolderCreateSerializer(parent_folder.get_children(), many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='move-folder',
            url_name='move-folder', permission_classes=[IsAuthenticatedOwnerUser])
    def move_folder(self, request, pk):
        """ Move the folder content to another folder """

        actual_folder = self.get_object()

        id_new_parent_folder = request.POST.get('new_parent_folder', None)
        if id_new_parent_folder is None:
            return Response(
                {'message': 'The new_parent_folder field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_parent_folder = self.request.user.get_folder_by_id(id_new_parent_folder)

        if new_parent_folder is None:
            return Response(
                {'message': 'The destination folder does not exists. Check it and try again'},
                status=status.HTTP_404_NOT_FOUND
            )

        if new_parent_folder.pk == actual_folder.get_parent().pk:
            return Response(
                {'message': 'The new folder to be moved to must be different than current parent folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        if new_parent_folder.pk == actual_folder.pk:
            return Response(
                {'message': 'The new folder to be moved to must be different than current folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        if actual_folder.name in new_parent_folder.get_children_folder():
            return Response(
                {'message': 'The new folder to be moved to must be different name of the children folder'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        if Folder.move_folder_into_another(actual_folder, new_parent_folder) is True:
            return Response(
                {'message': 'Folder moved successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'An error occurred while moving the folder.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['patch'], url_path='move-to-recycle-bin',
            url_name='move-to-recycle-bin', permission_classes=[IsAuthenticatedOwnerUser])
    def move_to_recycle_bin(self, request, pk):
        """ move folder to the recycle bin and prepare for his elimination """
        element = self.get_object()
        try:
            element.disable_folder_and_children()
            return Response({'message': 'Folder and children moved to recycle bin. Will be delete in 3 days'})
        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='recover-folder',
            url_name='recover-folder', permission_classes=[IsAuthenticatedOwnerUser])
    def recover_folder(self, request, pk):
        """ move folder to the recycle bin and prepare for his elimination """
        element = self.get_object()
        try:
            element.activate_folder_and_children()
            return Response({'message': 'Folder and children recover successfully'})
        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete-folder',
            url_name='delete-folder', permission_classes=[IsAuthenticatedOwnerUser])
    def delete_folder(self, request, pk):
        """ move folder to the recycle bin and prepare for his elimination """
        element = self.get_object()
        try:
            folder_manager = FolderManager(element)
            folder_manager._delete_folder()
            return Response({'message': 'Folder and children deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_400_BAD_REQUEST)
