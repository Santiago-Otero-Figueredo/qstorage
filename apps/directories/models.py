from typing import Optional, TYPE_CHECKING

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings

from apps.core.models import BaseProjectModel

from .utils.folder_manager import (update_children_folders,
                                  update_route_parent_folder_and_children,
                                  move_folders_in_media)

# Create your models here.
from treebeard.mp_tree import MP_Node

import os

if TYPE_CHECKING:
    from apps.users.models import User


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
    def create_folder(owner_user: 'User', name: str) -> 'Folder':
        """
            Create a new folder to a user

            Params:
                owner_user(User): User to whom the folder will be created
                name(str): Name of the folder
                route(str): Route of folder

            Return:
                root(Folder): The new folder created
        """
        return Folder.objects.create(owner_user=owner_user, name=name)

    @staticmethod
    def create_folder_and_assign_to_parent(owner_user: 'User', name: str, parent_folder: 'Folder') -> 'Folder':
        """
            Create a new folder to a user and assign to parent folder

            Params:
                owner_user(User): User to whom the folder will be created
                name(str): Name of the folder
                route(str): Route of folder

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
            folder_update.update(route=f'{new_parent_folder.route}{new_parent_folder.name}')

            update_route_parent_folder_and_children(folder_update.first())
            move_folders_in_media(old_path, folder_update.first().get_path_folder())
            return True
        except Exception:
            return False

    def get_path_parent_folder(self) -> str:
        """
            Return the path of the folder parent folder

            Return:
                path(str): path of the parent folder
        """
        user_path = f'{self.owner_user.pk}'
        ancestors = self.get_ancestors().values_list('name', flat=True)

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

        return f'{self.get_path_parent_folder()}/{self.name}'


@receiver(pre_save, sender=Folder)
def pre_save_assign_root_folder(sender, instance, *args, **kwargs):

    media_root_path = settings.MEDIA_ROOT

    user_path = f'{instance.owner_user.pk}'
    ancestors = instance.get_ancestors().values_list('name', flat=True)

    list_path = [user_path]

    if ancestors:
        list_path = list_path + ancestors[1::]

    path_folder = "/".join(list_path)

    media_patch_folder = os.path.join(media_root_path, path_folder)
    if ancestors:
        media_patch_folder = os.path.join(media_root_path, path_folder, instance.name)

    if instance.pk is None:
        os.umask(0)
        os.makedirs(media_patch_folder, mode=0o777)
    elif instance.get_children_count() > 0 or instance.is_leaf() and not instance.is_root():
        update_children_folders(instance)

    instance.route = f'{path_folder}/'
    instance.old_name = instance.name


class File(BaseProjectModel):
    parent_folder = models.ForeignKey(
        Folder,
        verbose_name='Parent folder',
        related_name='files',
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=30)
    size = models.PositiveBigIntegerField()


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
