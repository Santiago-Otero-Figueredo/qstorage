from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin, AbstractUser

from apps.core.models import BaseProjectModel
from apps.directories.models import Folder

class User(AbstractUser, PermissionsMixin, BaseProjectModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email}"


    @staticmethod
    def get_user_by_email(email):
        """
            Return the user whit the email received as parameter

            Params:
                email(str): email used to search

            Return:
                user(User): User whit the email received as parameter or None if does not exist
        """

        try:
            return User.objects.get(email=email)
        except:
            return None


@receiver(post_save, sender=User)
def assign_root_folder(sender, instance, created, *args, **kwargs):


    if created:        
        Folder.create_root_folder_to_created_user(instance)

    
#@receiver(pre_save, sender=User)
#def create_media_folder_user(sender, instance, *args, **kwargs):

    