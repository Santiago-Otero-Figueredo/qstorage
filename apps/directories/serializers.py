from dataclasses import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Folder, File


class FolderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('name', 'is_active')

    def save(self, **kwargs):
        method = self.context.get('method')
        owner_user = self.context.get('owner_user')

        if method != 'POST':
            return super().save(**kwargs)

        pay_load = ({**self.validated_data, 'owner_user': owner_user, **kwargs, 'parent_folder': self.instance})

        pay_load.pop('is_active')

        return Folder.create_folder_and_assign_to_parent(**pay_load)

    def validate(self, data):

        duplicate = self.instance.get_children().filter(name=data['name']).exists()
        duplicate_siblings = self.instance.get_siblings().filter(name=data['name']).exists()

        if duplicate or duplicate_siblings:
            raise ValidationError("There cannot be two folders with the same name")

        return data


class FileSerializer(serializers.ModelSerializer):
    #parent_folder = serializers.PrimaryKeyRelatedField(queryset=Folder.get_all())

    def validate(self, data):

        # new_parent_folder = data.get('parent_folder', None)
        complete_name = f'{data["name"]}.{self.instance.details.type}'
        # if new_parent_folder is not None and new_parent_folder != self.instance.parent_folder:

        #     duplicate = new_parent_folder.get_all_files().filter(name=complete_name).exists()
        #     if duplicate:
        #         raise ValidationError("There cannot be two files with the same name")

        if self.instance.name != complete_name:
            duplicate = self.instance.parent_folder.get_all_files().filter(name=complete_name).exists()

            if duplicate:
                raise ValidationError("There cannot be two files with the same name")

        return data

    class Meta:
        model = File
        fields = ['pk', 'name', 'file']