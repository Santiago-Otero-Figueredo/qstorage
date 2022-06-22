from enum import unique
from importlib.resources import path
from venv import create
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings


from apps.core.models import BaseProjectModel

from apps.directories.utils.folder_manager import update_children_folders

# Create your models here.
from treebeard.mp_tree import MP_Node



def user_entity_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'



class Folder(MP_Node, BaseProjectModel):
    owner_user = models.ForeignKey('users.User', verbose_name='Owner user', related_name='own_entity_directories', on_delete=models.CASCADE)
    collaboration_users = models.ManyToManyField('users.User', verbose_name='Collaborators', related_name='shared_entity_directories', through='directories.collaboration')
    name = models.CharField(max_length=255, verbose_name='Name')
    route = models.CharField(max_length=255, verbose_name='Path of entity')

    node_order_by = ['name']

    class Meta:
        unique_together = ('path', 'name')

    def __str__(self):
        return 'Category: {}'.format(self.name)


    @staticmethod
    def create_folder(owner_user:'User', name:str):
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
    def create_folder_and_assign_to_parent(owner_user:'User', name:str, parent_folder:'Folder') -> 'Folder':
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
    def create_root_folder_to_created_user(user:'User') -> 'Folder':
        """
            Create the root folder to a new user created and return it

            Params:
                user(User): User to whom the folder will be created
            
            Return:
                root(Folder): The root folder created
        """

        return Folder.add_root(owner_user=user, name='/', route='/')


    @staticmethod
    def get_root_folder_by_user(user:'User') -> 'Folder':
        """
            Return the root folder of an user

            Params:
                user(User): User to get te root folder
            
            Return:
                root(Folder): The root folder created or None if does not exist
        """

        try:
            return Folder.objects.filter(owner_user=user).first().get_root_nodes().first()
        except:
            return None
            


@receiver(pre_save, sender=Folder)
def pre_save_assign_root_folder(sender, instance, *args, **kwargs):
    import os, shutil, errno

    MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", None)

    user_path = f'{instance.owner_user.pk}'
    ancestors = instance.get_ancestors().values_list('name', flat=True)

    has_children = (instance.get_children_count() > 0)

    
    list_path = [user_path]

    if ancestors:
        list_path = list_path + ancestors[1::]

    path_folder = "/".join(list_path)
    media_patch_folder = os.path.join(MEDIA_ROOT, path_folder)

    if not has_children:
        os.umask(0)
        os.makedirs(media_patch_folder, mode=0o777)

    instance.route = f'{path_folder}/'


@receiver(post_save, sender=Folder)
def post_save_update_children_folders(sender, created, instance, *args, **kwargs):

    if instance.get_children_count() > 0:
        update_children_folders(instance)
       


class File(BaseProjectModel):
    parent_folder = models.ForeignKey(Folder, verbose_name='Parent folder', related_name='files', on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    size = models.PositiveBigIntegerField()


class Collaboration(BaseProjectModel):
    user = models.ForeignKey('users.User', verbose_name='Collaborator user', related_name='collaboration_users', on_delete=models.PROTECT)
    folder = models.ForeignKey(Folder, verbose_name='Folder', related_name='collaboration_folder', on_delete=models.PROTECT)
    comment = models.TextField()


    

    