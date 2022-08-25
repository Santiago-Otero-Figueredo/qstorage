from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.core.models import BaseProjectModel

from typing import TYPE_CHECKING, List, Set

from ..models import Folder
from ..utils.file_manager import FileManager

import os

if TYPE_CHECKING:
    from apps.users.models import User


def get_upload_path(instance, filename):
    return os.path.join(f'{instance.parent_folder.get_path_folder()}/{filename}')


class File(BaseProjectModel):
    parent_folder = models.ForeignKey(
        Folder,
        verbose_name='Parent folder',
        related_name='files',
        on_delete=models.CASCADE
    )
    details = models.OneToOneField(
        'directories.Detail',
        verbose_name='Details file',
        related_name='file_details',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, verbose_name='Name of the file', blank=True)
    file = models.FileField(upload_to=get_upload_path)

    @staticmethod
    def get_all_files_by_user(user: 'User') -> QuerySet['File']:
        """ Return all the files in all folders of a user received

            Parameter:
                user(User): user used to make the search

            Return
                filer(QuerySet['File']): All files of the user
        """

        return File.objects.filter(parent_folder__owner_user__pk=user.pk)

    @staticmethod
    def get_all_files_by_user_and_list_ids(user: 'User', list_ids: List['int']) -> QuerySet['File']:
        """ Return all the files in all folders of a user received and a list of ids

            Parameter:
                user(User): user used to make the search
                list_ids(List['int']): list of ides of files to search

            Return
                filer(QuerySet['File']): All files of the user
        """

        return File.get_all_files_by_user(user).filter(pk__in=list_ids)

    @staticmethod
    def get_all_files_names_by_user_and_list_ids(user: 'User', list_ids: List['int']) -> Set[str]:
        """ Return all the files names in all folders of a user received and a list of ids

            Parameter:
                user(User): user used to make the search
                list_ids(List['int']): list of ides of files to search

            Return
                files_names(Set[str]): All files names of the user
        """

        return set(File.get_all_files_by_user_and_list_ids(user, list_ids).values_list('name', flat=True))

    @staticmethod
    def get_all_name_files_by_list_ids(list_ids: List['int']) -> Set[str]:
        """ Return all the name files in the list of ids

            Parameter:
                list_ids(List['int']): list of ides of files to search

            Return
                names(Set[str]): All folder pk
        """

        return set(File.get_elements_by_list_id(list_ids).values_list('name', flat=True))

    @staticmethod
    def get_all_pk_parent_folder_list_ids_files(list_ids: List['int']) -> Set[int]:
        """ Return all the pk parent folder of the files in the list of ids

            Parameter:
                list_ids(List['int']): list of ides of files to search

            Return
                pk_folders(Set[int]): All folder pk
        """
        return set(File.get_elements_by_list_id(list_ids).values_list('parent_folder__pk', flat=True))

    @staticmethod
    def move_many_files_into_another_folder(files_ids: List[int], new_parent_folder: 'Folder') -> bool:
        """
            Move a files into another folder and return if the result of the action.

            Parameters:
                files_ids(List[int]): The list of ids files to be moved
                new_parent_folder(Folder): The new parent folder where it will be moved

            Return:
                result(bool): True if success or False otherwise
        """
        try:
            files_to_move = File.get_elements_by_list_id(files_ids)
            for file in files_to_move:
                file.parent_folder = new_parent_folder
                file.save()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def disabled_many_files(files_id: List[int]) -> bool:
        """
            Disable many files and return if the result of the action.

            Parameters:
                files_id(Folder): The list of ids files to be moved to the recicle bin

            Return:
                result(bool): True if success or False otherwise

        """
        try:
            files_to_disable = File.get_elements_by_list_id(files_id)
            files_to_disable.update(is_active=False)
            return True
        except Exception:
            return False

    @staticmethod
    def recover_many_files(files_id: List[int]) -> bool:
        """
            Activate many files and return if the result of the action.

            Parameters:
                files_id(Folder): The list of ids files to be moved to the recicle bin

            Return:
                result(bool): True if success or False otherwise

        """
        try:
            files_to_disable = File.get_elements_by_list_id(files_id)
            files_to_disable.update(is_active=True)
            return True
        except Exception:
            return False

    @staticmethod
    def delete_many_files(files_id: List[int]) -> bool:
        """
            Delete a Files return if the result of the action.

            Parameters:
                files_id(List[int]): The list of ids files to be delete

            Return:
                result(bool): True if success or False otherwise
        """

        try:
            files_to_disable = File.get_elements_by_list_id(files_id)
            for file in files_to_disable:
                file_manager = FileManager(actual_file=file)
                file_manager._delete_folder()
            return True
        except Exception:
            return False

    def get_full_name(self) -> str:
        """ Return the name and the extension of the file """
        if '.' not in self.name:
            return f'{self.name}.{self.details.type}'
        return self.name

    def get_full_path(self) -> str:
        """ Return the full path of the file """

        return f'{self.parent_folder.get_absolute_path_folder()}/{self.get_full_name()}'

    def save(self, **kwargs):
        # here we use os.rename then change the name of the file
        # add condition to do this, I suggest requerying the model
        # and checking if label is different
        if self.pk:  # Need this to mitigate error using self.pk

            old_file = File.get_by_id(self.pk)

            file_manager = FileManager(self, old_file)
            file_manager._process_save()

        return super(File, self).save(**kwargs)


@receiver(pre_save, sender=File)
def pre_save_assign_root_folder(sender, instance, update_fields, *args, **kwargs):

    if instance.pk is None:
        name_file, extension = os.path.splitext(instance.file.name)
        instance.name = f'{name_file}{extension}'
        detail = Detail.objects.create(
            type=extension.replace('.', ''),
            size=instance.file.size
        )
        instance.details = detail
    else:
        instance.name = instance.get_full_name()


class Detail(BaseProjectModel):
    type = models.CharField(max_length=30, default='NN')
    size = models.PositiveBigIntegerField(default=0)
