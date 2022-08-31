from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import File
from apps.directories.models.folder import Folder
from apps.directories.test.files.test_crud import FileCRUDAPITest

URL_MOVE_TO_RECICLE_BIN = 'directories:folders-move-to-recycle-bin'
URL_RECOVER_FOLDER = 'directories:folders-recover-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FileCRUDAPITest):

    def test_01_move_recicle_bin_folder_with_files(self):
        """ Testing to move to recicle bin many folders with files """

        payload = {
            'folders_to_disable': [self.peripherals.pk, self.gpu.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        folder_peripherals_moved = Folder.get_by_id(self.peripherals.pk)
        folder_gpu_moved = Folder.get_by_id(self.gpu.pk)

        folder_nvidia_moved = Folder.get_by_id(self.nvidia.pk)
        folder_g_amd_moved = Folder.get_by_id(self.g_amd.pk)
        folder_rtx_moved = Folder.get_by_id(self.rtx.pk)
        folder_ti_rtx_moved = Folder.get_by_id(self.ti_rtx.pk)
        folder_gtx_moved = Folder.get_by_id(self.gtx.pk)
        folder_ti_gtx_moved = Folder.get_by_id(self.ti_gtx.pk)

        file_series_1000_moved = File.get_by_id(self.f_series_1000.pk)
        file_series_2000_moved = File.get_by_id(self.f_series_2000.pk)
        file_series_4000_moved = File.get_by_id(self.f_series_4000.pk)
        file_series_5000_moved = File.get_by_id(self.f_series_5000.pk)
        file_2060_moved = File.get_by_id(self.f_2060.pk)
        file_1070_ti_moved = File.get_by_id(self.f_1070_ti.pk)
        file_1080_ti_moved = File.get_by_id(self.f_1080_ti.pk)
        file_2060_ti_moved = File.get_by_id(self.f_2060_ti.pk)
        file_3060_ti_moved = File.get_by_id(self.f_3060_ti.pk)
        file_1030_moved = File.get_by_id(self.f_1030.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(folder_peripherals_moved.is_active)
        self.assertFalse(folder_gpu_moved.is_active)
        self.assertFalse(folder_nvidia_moved.is_active)
        self.assertFalse(folder_g_amd_moved.is_active)
        self.assertFalse(folder_rtx_moved.is_active)
        self.assertFalse(folder_ti_rtx_moved.is_active)
        self.assertFalse(folder_gtx_moved.is_active)
        self.assertFalse(folder_ti_gtx_moved.is_active)
        self.assertFalse(file_series_1000_moved.is_active)
        self.assertFalse(file_series_2000_moved.is_active)
        self.assertFalse(file_series_4000_moved.is_active)
        self.assertFalse(file_series_5000_moved.is_active)
        self.assertFalse(file_2060_moved.is_active)
        self.assertFalse(file_1070_ti_moved.is_active)
        self.assertFalse(file_1080_ti_moved.is_active)
        self.assertFalse(file_2060_ti_moved.is_active)
        self.assertFalse(file_3060_ti_moved.is_active)
        self.assertFalse(file_1030_moved.is_active)

    def test_02_recover_folder_with_files(self):
        """ Testing to recover many folders with files """

        payload = {
            'folders_to_recover': [self.peripherals.pk, self.gpu.pk]
        }

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        folder_peripherals_moved = Folder.get_by_id(self.peripherals.pk)
        folder_gpu_moved = Folder.get_by_id(self.gpu.pk)

        folder_nvidia_moved = Folder.get_by_id(self.nvidia.pk)
        folder_g_amd_moved = Folder.get_by_id(self.g_amd.pk)
        folder_rtx_moved = Folder.get_by_id(self.rtx.pk)
        folder_ti_rtx_moved = Folder.get_by_id(self.ti_rtx.pk)
        folder_gtx_moved = Folder.get_by_id(self.gtx.pk)
        folder_ti_gtx_moved = Folder.get_by_id(self.ti_gtx.pk)

        file_series_1000_moved = File.get_by_id(self.f_series_1000.pk)
        file_series_2000_moved = File.get_by_id(self.f_series_2000.pk)
        file_series_4000_moved = File.get_by_id(self.f_series_4000.pk)
        file_series_5000_moved = File.get_by_id(self.f_series_5000.pk)
        file_2060_moved = File.get_by_id(self.f_2060.pk)
        file_1070_ti_moved = File.get_by_id(self.f_1070_ti.pk)
        file_1080_ti_moved = File.get_by_id(self.f_1080_ti.pk)
        file_2060_ti_moved = File.get_by_id(self.f_2060_ti.pk)
        file_3060_ti_moved = File.get_by_id(self.f_3060_ti.pk)
        file_1030_moved = File.get_by_id(self.f_1030.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(folder_peripherals_moved.is_active)
        self.assertTrue(folder_gpu_moved.is_active)
        self.assertTrue(folder_nvidia_moved.is_active)
        self.assertTrue(folder_g_amd_moved.is_active)
        self.assertTrue(folder_rtx_moved.is_active)
        self.assertTrue(folder_ti_rtx_moved.is_active)
        self.assertTrue(folder_gtx_moved.is_active)
        self.assertTrue(folder_ti_gtx_moved.is_active)
        self.assertTrue(file_series_1000_moved.is_active)
        self.assertTrue(file_series_2000_moved.is_active)
        self.assertTrue(file_series_4000_moved.is_active)
        self.assertTrue(file_series_5000_moved.is_active)
        self.assertTrue(file_2060_moved.is_active)
        self.assertTrue(file_1070_ti_moved.is_active)
        self.assertTrue(file_1080_ti_moved.is_active)
        self.assertTrue(file_2060_ti_moved.is_active)
        self.assertTrue(file_3060_ti_moved.is_active)
        self.assertTrue(file_1030_moved.is_active)
