from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder, File
from apps.directories.test.files.test_crud import FileCRUDAPITest

import os.path

URL_MOVE_FOLDER = 'directories:folders-move-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FileMoveTest(FileCRUDAPITest):

    def test_prueba(self):
        pass