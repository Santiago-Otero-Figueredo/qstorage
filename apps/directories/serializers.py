from os import dup
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Folder


class FolderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('name', 'owner_user')

    def save(self, **kwargs):
        method = self.context.get('method')

        if method != 'POST':
            return super().save(**kwargs)

        pay_load = ({**self.validated_data, **kwargs, 'parent_folder':self.instance})       
        print(pay_load)
        return Folder.create_folder_and_assign_to_parent(**pay_load)


    def validate(self, data):

        duplicate = self.instance.get_children().filter(name=data['name']).exists()
        if duplicate:
            raise ValidationError("There cannot be two folders with the same name")

        return data
