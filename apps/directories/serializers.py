from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Folder


class FolderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('name',)

    def save(self, **kwargs):
        method = self.context.get('method')
        owner_user = self.context.get('owner_user')

        if method != 'POST':
            return super().save(**kwargs)

        pay_load = ({**self.validated_data, 'owner_user': owner_user, **kwargs, 'parent_folder': self.instance})

        return Folder.create_folder_and_assign_to_parent(**pay_load)

    def validate(self, data):

        duplicate = self.instance.get_children().filter(name=data['name']).exists()
        duplicate_siblings = self.instance.get_siblings().filter(name=data['name']).exists()

        if duplicate or duplicate_siblings:
            raise ValidationError("There cannot be two folders with the same name")

        return data
