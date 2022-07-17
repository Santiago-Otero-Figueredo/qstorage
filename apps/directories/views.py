from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import FolderCreateSerializer
from .permissions import IsAuthenticatedOwnerUser


class FolderVS(ModelViewSet):

    serializer_class = FolderCreateSerializer
    permission_classes = [IsAuthenticatedOwnerUser]

    def get_queryset(self):
        return self.request.user.own_entity_directories.all()

    @action(detail=True, methods=['post'], url_path='create-folder',
            url_name='create-folder', permission_classes=[IsAuthenticatedOwnerUser])
    def create_new_folder(self, request, pk):
        """ Create a new folder inside another using the pk to get the parent folder"""

        parent_folder = self.get_object()

        if parent_folder is None:
            return Response({'message': 'The folder does not exist'}, status=status.HTTP_400_BAD_REQUEST)

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

        if parent_folder is None:
            return Response({'message': 'The folder does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FolderCreateSerializer(parent_folder.get_children(), many=True)

        return Response(serializer.data)
