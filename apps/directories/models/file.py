from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.core.models import BaseProjectModel

from typing import TYPE_CHECKING

from ..models import Folder

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
    name = models.CharField(max_length=255, verbose_name='Name of the file')
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

    def save(self, **kwargs):
        # here we use os.rename then change the name of the file
        # add condition to do this, I suggest requerying the model
        # and checking if label is different
        if self.pk:  # Need this to mitigate error using self.pk

            print("###################### self: ",self)
            old_file = File.get_by_id(self.pk)
            old_folder = old_file.parent_folder.get_path_folder()
            new_folder = self.parent_folder.get_path_folder()

            new_file_name = self.name
            old_file_name = old_file.name

            print("new_file_name: ", new_file_name, ' old_file_name: ', old_file_name)
            if old_folder != new_folder:

                new_rename = f'{new_folder}/{new_file_name}'

                old_path = old_folder
                old_rename = f'{old_path}/{new_file_name}'

                print("##########: new_rename", new_rename , "=old_rename=", old_rename)
                # os.rename(path, rename)
                # file = File(open(rename))
                # self.file.save(self.label, file)

            if old_file_name != new_file_name:
                print("IMPLEMENTAR CAMBIO DE NOMBRE")

        return super(File, self).save(**kwargs)


@receiver(pre_save, sender=File)
def pre_save_assign_root_folder(sender, instance, update_fields, *args, **kwargs):

    if instance.pk is None:
        name_file, extension = os.path.splitext(instance.file.name)
        instance.name = f'{name_file}{extension}'
        detail = Detail.objects.create(
            type=extension.replace('.',''),
            size=instance.file.size
        )
        instance.details = detail


class Detail(BaseProjectModel):
    type = models.CharField(max_length=30, default='NN')
    size = models.PositiveBigIntegerField(default=0)
