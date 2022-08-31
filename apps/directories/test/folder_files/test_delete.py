from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder, File
from apps.directories.test.files.test_crud import FileCRUDAPITest

import os.path

URL_DELETE_FOLDER = 'directories:folders-delete-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FileCRUDAPITest):

    def test_01_delete_folder_with_files(self):
        """ Testing the delete folder whit files """

        payload = {
            'folders_to_delete': [self.peripherals.pk, self.gpu.pk]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)

        media_path_peripherals_folder = f'{settings.MEDIA_ROOT_TEST}{self.peripherals.get_path_folder()}'
        media_path_gpu_folder = f'{settings.MEDIA_ROOT_TEST}{self.gpu.get_path_folder()}'
        media_path_nvidia_folder = f'{settings.MEDIA_ROOT_TEST}{self.nvidia.get_path_folder()}'
        media_path_g_amd_folder = f'{settings.MEDIA_ROOT_TEST}{self.g_amd.get_path_folder()}'
        media_path_rtx_folder = f'{settings.MEDIA_ROOT_TEST}{self.rtx.get_path_folder()}'
        media_path_ti_rtx_folder = f'{settings.MEDIA_ROOT_TEST}{self.ti_rtx.get_path_folder()}'
        media_path_gtx_2600_folder = f'{settings.MEDIA_ROOT_TEST}{self.gtx.get_path_folder()}'
        media_path_ti_gtx_3600_folder = f'{settings.MEDIA_ROOT_TEST}{self.ti_gtx.get_path_folder()}'

        media_file_series_1000_delete = self.f_series_1000.get_full_path()
        media_file_series_2000_delete = self.f_series_2000.get_full_path()
        media_file_series_4000_delete = self.f_series_4000.get_full_path()
        media_file_series_5000_delete = self.f_series_5000.get_full_path()
        media_file_2060_delete = self.f_2060.get_full_path()
        media_file_1070_ti_delete = self.f_1070_ti.get_full_path()
        media_file_1080_ti_delete = self.f_1080_ti.get_full_path()
        media_file_2060_ti_delete = self.f_2060_ti.get_full_path()
        media_file_3060_ti_delete = self.f_3060_ti.get_full_path()
        media_file_1030_delete = self.f_1030.get_full_path()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder, payload)

        folder_peripherals = Folder.get_by_id(self.peripherals.pk)
        folder_gpu = Folder.get_by_id(self.gpu.pk)

        folder_nvidia = Folder.get_by_id(self.nvidia.pk)
        folder_g_amd = Folder.get_by_id(self.g_amd.pk)
        folder_rtx = Folder.get_by_id(self.rtx.pk)
        folder_ti_rtx = Folder.get_by_id(self.ti_rtx.pk)
        folder_gtx = Folder.get_by_id(self.gtx.pk)
        folder_ti_gtx = Folder.get_by_id(self.ti_gtx.pk)

        file_series_1000 = File.get_by_id(self.f_series_1000.pk)
        file_series_2000 = File.get_by_id(self.f_series_2000.pk)
        file_series_4000 = File.get_by_id(self.f_series_4000.pk)
        file_series_5000 = File.get_by_id(self.f_series_5000.pk)
        file_2060 = File.get_by_id(self.f_2060.pk)
        file_1070_ti = File.get_by_id(self.f_1070_ti.pk)
        file_1080_ti = File.get_by_id(self.f_1080_ti.pk)
        file_2060_ti = File.get_by_id(self.f_2060_ti.pk)
        file_3060_ti = File.get_by_id(self.f_3060_ti.pk)
        file_1030 = File.get_by_id(self.f_1030.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(folder_peripherals)
        self.assertIsNone(folder_gpu)
        self.assertIsNone(folder_nvidia)
        self.assertIsNone(folder_g_amd)
        self.assertIsNone(folder_rtx)
        self.assertIsNone(folder_ti_rtx)
        self.assertIsNone(folder_gtx)
        self.assertIsNone(folder_ti_gtx)
        self.assertIsNone(file_series_1000)
        self.assertIsNone(file_series_2000)
        self.assertIsNone(file_series_4000)
        self.assertIsNone(file_series_5000)
        self.assertIsNone(file_2060)
        self.assertIsNone(file_1070_ti)
        self.assertIsNone(file_1080_ti)
        self.assertIsNone(file_2060_ti)
        self.assertIsNone(file_3060_ti)
        self.assertIsNone(file_1030)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_peripherals_folder))
        self.assertFalse(os.path.exists(media_path_gpu_folder))
        self.assertFalse(os.path.exists(media_path_nvidia_folder))
        self.assertFalse(os.path.exists(media_path_g_amd_folder))
        self.assertFalse(os.path.exists(media_path_rtx_folder))
        self.assertFalse(os.path.exists(media_path_ti_rtx_folder))
        self.assertFalse(os.path.exists(media_path_gtx_2600_folder))
        self.assertFalse(os.path.exists(media_path_ti_gtx_3600_folder))
        self.assertFalse(os.path.exists(media_file_series_1000_delete))
        self.assertFalse(os.path.exists(media_file_series_2000_delete))
        self.assertFalse(os.path.exists(media_file_series_4000_delete))
        self.assertFalse(os.path.exists(media_file_series_5000_delete))
        self.assertFalse(os.path.exists(media_file_2060_delete))
        self.assertFalse(os.path.exists(media_file_1070_ti_delete))
        self.assertFalse(os.path.exists(media_file_1080_ti_delete))
        self.assertFalse(os.path.exists(media_file_2060_ti_delete))
        self.assertFalse(os.path.exists(media_file_3060_ti_delete))
        self.assertFalse(os.path.exists(media_file_1030_delete))
