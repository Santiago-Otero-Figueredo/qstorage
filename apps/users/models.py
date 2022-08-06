from django.db import models
from django.db.models import QuerySet
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin, AbstractUser

from apps.core.models import BaseProjectModel
from apps.directories.models import Folder

from typing import Optional, List, Set


class User(AbstractUser, PermissionsMixin, BaseProjectModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email}"

    @staticmethod
    def get_user_by_email(email) -> Optional['User']:
        """
            Return the user whit the email received as parameter

            Params:
                email(str): email used to search

            Return:
                user(User): User whit the email received as parameter or None if does not exist
        """

        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_all_folders_except_root(self) -> 'QuerySet[Folder]':
        """
            Return all folders of the user except for the root

            Return:
                folders(Queryset<Folder>): user's folders
        """
        return self.own_entity_directories.exclude(name=settings.ROOT_NAME_FOLDER)

    def get_all_folders(self) -> 'QuerySet[Folder]':
        """
            Return all folders of the user

            Return:
                folders(Queryset<Folder>): user's folders
        """
        return self.own_entity_directories.all()

    def is_owner_folder(self, id_folder: int) -> bool:
        """
            Return if the user is owner of the folder

            Parameter:
                id_folder(int): id of the folder to validate

            Return:
                owner(bool): is owner
        """
        return self.own_entity_directories.filter(pk=id_folder).exists()

    def get_folder_by_id(self, id_folder: int) -> Optional[Folder]:
        """
            Return if the user is owner of the folder

            Parameter:
                id_folder(int): id of the folder to get

            Return:
                folder(Folder): Folder if exists, or None otherwise
        """
        try:
            return self.own_entity_directories.get(pk=id_folder)
        except Folder.DoesNotExist:
            return None

    def get_all_folders_by_list_ids(self, list_ids: List[int]) -> 'QuerySet[Folder]':
        """
            Return all folders of the user that is contained in the list of ids

            Parameters:
                list_ids(List[int]): List of ids to search

            Return:
                folders(Queryset<Folder>): user's folders
        """
        return self.own_entity_directories.filter(pk__in=list_ids)

    def get_all_names_of_folders_by_list_ids(self, list_ids: List[int]) -> Set[str]:
        """
            Returns the names of all the folders of the received
            folders as pk in the list of identifiers of the user

            Parameters:
                list_ids(List[int]): List of folder pk to get the names

            Return:
                list_ids_parents(Set[int]): Set of folders names
        """
        folders = self.get_all_folders_by_list_ids(list_ids)

        list_parent_names = set(folders.values_list('name', flat=True))

        return list_parent_names


@receiver(post_save, sender=User)
def assign_root_folder(sender, instance, created, *args, **kwargs):

    if created:
        Folder.create_root_folder_to_created_user(instance)
