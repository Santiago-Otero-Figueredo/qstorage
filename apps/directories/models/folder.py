from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


from apps.core.models import BaseProjectModel

from ..utils.folder_manager import (FolderManager,
                                    move_folders_in_media)

from treebeard.mp_tree import MP_Node

from typing import List, Optional, TYPE_CHECKING, Set


if TYPE_CHECKING:
    from apps.users.models import User
    from apps.directories.models import File


class Folder(MP_Node, BaseProjectModel):
    owner_user = models.ForeignKey(
        'users.User',
        verbose_name='Owner user',
        related_name='own_entity_directories',
        on_delete=models.CASCADE
    )
    collaboration_users = models.ManyToManyField(
        'users.User',
        verbose_name='Collaborators',
        related_name='shared_entity_directories',
        through='directories.collaboration'
    )
    name = models.CharField(max_length=255, verbose_name='Name')
    route = models.CharField(max_length=255, verbose_name='Path of entity')
    old_name = models.CharField(max_length=255, verbose_name='Old name', default='')

    node_order_by = ['name']

    class Meta:
        unique_together = ('path', 'name')

    def __str__(self):
        return 'Category: {}'.format(self.name)

    @staticmethod
    def create_folder_and_assign_to_parent(owner_user: 'User', name: str, parent_folder: 'Folder') -> 'Folder':
        """
            Create a new folder to a user and assign to parent folder

            Params:
                owner_user(User): User to whom the folder will be created
                name(str): Name of the folder
                parent_folder(Folder): Parent folder of the new folder

            Return:
                root(Folder): The new folder created
        """

        return parent_folder.add_child(owner_user=owner_user, name=name)

    @staticmethod
    def create_root_folder_to_created_user(user: 'User') -> 'Folder':
        """
            Create the root folder to a new user created and return it

            Params:
                user(User): User to whom the folder will be created

            Return:
                root(Folder): The root folder created
        """

        return Folder.add_root(owner_user=user, name=settings.ROOT_NAME_FOLDER, route=settings.ROOT_NAME_FOLDER)

    @staticmethod
    def get_root_folder_by_user(user: 'User') -> Optional['Folder']:
        """
            Return the root folder of an user

            Params:
                user(User): User to get te root folder

            Return:
                root(Folder): The root folder created or None if does not exist
        """

        try:
            return Folder.objects.filter(owner_user=user).first().get_root_nodes().first()
        except Folder.DoesNotExist:
            return None

    @staticmethod
    def move_folder_into_another(folder: 'Folder', new_parent_folder: 'Folder') -> bool:
        """
            Move a Folder with all its contents into another and return if the result of the action.

            Parameters:
                folder(Folder): The folder to be moved
                new_parent_folder(Folder): The new parent folder where it will be moved
        """
        try:
            folder.move(new_parent_folder, pos='sorted-child')
            old_path = folder.get_path_folder()

            folder_update = Folder.objects.filter(pk=folder.pk)
            folder_update.update(route=f'{new_parent_folder.route}{new_parent_folder.name}/')

            folder_update.first().update_route_parent_folder_and_children()
            move_folders_in_media(old_path, folder_update.first().get_path_folder())
            return True
        except Exception:
            return False

    @staticmethod
    def move_many_folder_into_another(folders_id: List[int], new_parent_folder: 'Folder') -> bool:
        """
            Move a Folder with all its contents into another and return if the result of the action.

            Parameters:
                folders_id(List[int]): The list of ids folder to be moved
                new_parent_folder(Folder): The new parent folder where it will be moved

            Return:
                result(bool): True if success or False otherwise
        """
        try:
            folders_to_move = Folder.get_elements_by_list_id(folders_id)
            for folder in folders_to_move:
                Folder.move_folder_into_another(folder, new_parent_folder)
            return True
        except Exception:
            return False

    @staticmethod
    def delete_many_folder_and_children(folders_id: List[int]) -> bool:
        """
            Delete a Folder with all its contents and return if the result of the action.

            Parameters:
                folders_id(List[int]): The list of ids folder to be delete

            Return:
                result(bool): True if success or False otherwise
        """

        try:
            folders_to_disable = Folder.get_elements_by_list_id(folders_id)
            for folder in folders_to_disable:
                folder_manager = FolderManager(folder)
                folder_manager._delete_folder()
            return True
        except Exception:
            return False

    @staticmethod
    def get_all_pk_parents_in_list_ids(list_ids: List[int]) -> Set[int]:
        """
            Returns the pk of all the parent folders of the received
            folders as pk in the list of identifiers

            Parameters:
                list_ids(List[int]): List of folder pk to get the parent

            Return:
                list_ids_parents(Set[int]): Set of parents folders pk
        """
        folders = Folder.get_elements_by_list_id(list_ids)
        list_parent_pk = set()
        for folder in folders:
            list_parent_pk.add(folder.get_parent().pk)

        return list_parent_pk

    @staticmethod
    def disabled_many_folder_and_children(folders_id: List[int]) -> bool:
        """
            Disable many folders with all its contents into another and return if the result of the action.

            Parameters:
                folders_id(Folder): The list of ids folder to be moved to the recicle bin

            Return:
                result(bool): True if success or False otherwise

        """
        try:
            folders_to_disable = Folder.get_elements_by_list_id(folders_id)
            for folder in folders_to_disable:
                folder.disable_folder_and_children()
            return True
        except Exception:
            return False

    @staticmethod
    def recover_many_folder_and_children(folders_id: List[int]) -> bool:
        """
            Activate many folders with all its contents into another and return if the result of the action.

            Parameters:
                folders_id(Folder): The list of ids folder to be recover from the recicle bin

            Return:
                result(bool): True if success or False otherwise

        """
        try:
            folders_to_disable = Folder.get_elements_by_list_id(folders_id)
            for folder in folders_to_disable:
                folder.activate_folder_and_children()
            return True
        except Exception:
            return False

    def get_all_files(self) -> QuerySet['File']:
        """ Return all files associated to the actual folder """

        return self.files.all()

    def get_ancestors_folder(self) -> List[str]:
        """
            Return ancestors folder

            Return:
                ancestros(List[str]): list of the parent folders
        """

        return self.get_ancestors().values_list('name', flat=True)

    def get_children_folder(self) -> Set[str]:
        """
            Return children folder

            Return:
                children(Set[str]): list of children folders
        """

        return set(self.get_children().values_list('name', flat=True))

    def get_path_parent_folder(self) -> str:
        """
            Return the path of the folder parent folder

            Return:
                path(str): path of the parent folder
        """
        user_path = f'{self.owner_user.pk}'
        ancestors = self.get_ancestors_folder()

        list_path = [user_path]

        if ancestors:
            list_path = list_path + ancestors[1::]

        path_folder = "/".join(list_path)

        return path_folder

    def get_path_folder(self) -> str:
        """
            Return the path of the folder

            Return:
                path(str): path of the folder
        """
        path = self.get_path_parent_folder()
        if self.is_root() is False:
            return f'{path}/{self.name}'
        return path

    def update_route_parent_folder_and_children(self) -> None:
        """
            Update the path of the actual folder and his children. This method
            is used when the folder change his name or is moved
        """

        children_folders = self.get_children()
        children_folders.update(route=f'{self.route}{self.name}/')

        if self.get_children_count() > 0:
            for children in children_folders:
                children.update_route_parent_folder_and_children()

    def disable_folder_and_children(self) -> None:
        """ Disable the actual folder an his children"""
        folder = Folder.get_element_by_id_like_queryset(self.pk)
        folder.update(is_active=False)
        self.get_descendants().update(is_active=False)

    def activate_folder_and_children(self) -> None:
        """ Activate the actual folder an his children"""
        folder = Folder.get_element_by_id_like_queryset(self.pk)
        folder.update(is_active=True)
        self.get_descendants().update(is_active=True)


@receiver(pre_save, sender=Folder)
def pre_save_assign_root_folder(sender, instance, update_fields, *args, **kwargs):
    folder_manager = FolderManager(folder=instance)
    folder_manager._execute_pre_save_function()


class Collaboration(BaseProjectModel):
    user = models.ForeignKey('users.User',
        verbose_name='Collaborator user',
        related_name='collaboration_users',
        on_delete=models.PROTECT
    )
    folder = models.ForeignKey(
        Folder,
        verbose_name='Folder',
        related_name='collaboration_folder',
        on_delete=models.PROTECT
    )
    comment = models.TextField()
