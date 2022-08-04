from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder
from apps.directories.test.test_crud import FolderCRUDAPITest

URL_MOVE_TO_RECICLE_BIN = 'directories:folders-move-to-recycle-bin'
URL_RECOVER_FOLDER = 'directories:folders-recover-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FolderCRUDAPITest):

    def test_01_move_recicle_bin_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        url_move_folder = reverse(
            URL_MOVE_TO_RECICLE_BIN,
            kwargs={'pk': self.hardware.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_move_folder)
        response_2 = self.client.get(url_move_folder)
        response_3 = self.client.put(url_move_folder)
        response_4 = self.client.delete(url_move_folder)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_move_recicle_bin_folder_not_exists(self):
        """ Testing no list folder if does not exists """

        url_move_folder = reverse(
            URL_MOVE_TO_RECICLE_BIN,
            kwargs={'pk': 1000}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_move_leaf_folder_to_recicle_bin(self):
        """ Testing the disabled a leaf folder """

        url_move_folder = reverse(
            URL_MOVE_TO_RECICLE_BIN,
            kwargs={'pk': self.operative_system.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder)

        folder_moved = Folder.get_by_id(self.operative_system.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(folder_moved.is_active)


    def test_04_move_parent_folder_to_recicle_bin(self):
        """ Testing the disabled a parent folder and his children """

        url_move_folder = reverse(
            URL_MOVE_TO_RECICLE_BIN,
            kwargs={'pk': self.gpu.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder)

        folder_moved = Folder.get_by_id(self.operative_system.pk)
        gpu = Folder.get_by_id(self.gpu.pk)
        nvidia = Folder.get_by_id(self.nvidia.pk)
        n_series_1000 = Folder.get_by_id(self.n_series_1000.pk)
        n_series_2000 = Folder.get_by_id(self.n_series_2000.pk)
        n_series_3000 = Folder.get_by_id(self.n_series_3000.pk)
        n_series_4000 = Folder.get_by_id(self.n_series_4000.pk)
        g_amd = Folder.get_by_id(self.g_amd.pk)
        a_series_4000 = Folder.get_by_id(self.a_series_4000.pk)
        a_series_5000 = Folder.get_by_id(self.a_series_5000.pk)
        a_series_6000 = Folder.get_by_id(self.a_series_6000.pk)
        a_series_7000 = Folder.get_by_id(self.a_series_7000.pk)
        rtx = Folder.get_by_id(self.rtx.pk)
        ti_rtx = Folder.get_by_id(self.ti_rtx.pk)
        n_gpu_2060_ti = Folder.get_by_id(self.n_gpu_2060_ti.pk)
        n_gpu_3070_ti = Folder.get_by_id(self.n_gpu_3070_ti.pk)
        n_gpu_1070_ti = Folder.get_by_id(self.n_gpu_1070_ti.pk)
        n_gpu_1080_ti = Folder.get_by_id(self.n_gpu_1080_ti.pk)
        n_gpu_2060 = Folder.get_by_id(self.n_gpu_2060.pk)
        n_gpu_2070 = Folder.get_by_id(self.n_gpu_2070.pk)
        n_gpu_2080 = Folder.get_by_id(self.n_gpu_2080.pk)
        n_gpu_3080 = Folder.get_by_id(self.n_gpu_3080.pk)
        n_gpu_3060 = Folder.get_by_id(self.n_gpu_3060.pk)
        n_gpu_3070 = Folder.get_by_id(self.n_gpu_3070.pk)
        gtx = Folder.get_by_id(self.gtx.pk)
        ti_gtx = Folder.get_by_id(self.ti_gtx.pk)
        n_gpu_1030 = Folder.get_by_id(self.n_gpu_1030.pk)
        n_gpu_1650 = Folder.get_by_id(self.n_gpu_1650.pk)
        n_gpu_1080 = Folder.get_by_id(self.n_gpu_1080.pk)
        n_gpu_1060 = Folder.get_by_id(self.n_gpu_1060.pk)
        n_gpu_3090 = Folder.get_by_id(self.n_gpu_3090.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(gpu.is_active)
        self.assertFalse(nvidia.is_active)
        self.assertFalse(n_series_1000.is_active)
        self.assertFalse(n_series_2000.is_active)
        self.assertFalse(n_series_3000.is_active)
        self.assertFalse(n_series_4000.is_active)
        self.assertFalse(g_amd.is_active)
        self.assertFalse(a_series_4000.is_active)
        self.assertFalse(a_series_5000.is_active)
        self.assertFalse(a_series_6000.is_active)
        self.assertFalse(a_series_7000.is_active)
        self.assertFalse(rtx.is_active)
        self.assertFalse(ti_rtx.is_active)
        self.assertFalse(n_gpu_2060_ti.is_active)
        self.assertFalse(n_gpu_3070_ti.is_active)
        self.assertFalse(n_gpu_1070_ti.is_active)
        self.assertFalse(n_gpu_1080_ti.is_active)
        self.assertFalse(n_gpu_2060.is_active)
        self.assertFalse(n_gpu_2070.is_active)
        self.assertFalse(n_gpu_2080.is_active)
        self.assertFalse(n_gpu_3080.is_active)
        self.assertFalse(n_gpu_3060.is_active)
        self.assertFalse(n_gpu_3070.is_active)
        self.assertFalse(gtx.is_active)
        self.assertFalse(ti_gtx.is_active)
        self.assertFalse(n_gpu_1030.is_active)
        self.assertFalse(n_gpu_1650.is_active)
        self.assertFalse(n_gpu_1080.is_active)
        self.assertFalse(n_gpu_1060.is_active)
        self.assertFalse(n_gpu_3090.is_active)

    def test_05_recover_leaf_folder_to_recicle_bin(self):
        """ Testing the disabled a leaf folder """

        url_move_folder = reverse(
            URL_RECOVER_FOLDER,
            kwargs={'pk': self.operative_system.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder)

        folder_moved = Folder.get_by_id(self.operative_system.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(folder_moved.is_active)


    def test_06_move_parent_folder_to_recicle_bin(self):
        """ Testing the disabled a parent folder and his children """

        url_move_folder = reverse(
            URL_RECOVER_FOLDER,
            kwargs={'pk': self.gpu.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder)

        gpu = Folder.get_by_id(self.gpu.pk)
        nvidia = Folder.get_by_id(self.nvidia.pk)
        n_series_1000 = Folder.get_by_id(self.n_series_1000.pk)
        n_series_2000 = Folder.get_by_id(self.n_series_2000.pk)
        n_series_3000 = Folder.get_by_id(self.n_series_3000.pk)
        n_series_4000 = Folder.get_by_id(self.n_series_4000.pk)
        g_amd = Folder.get_by_id(self.g_amd.pk)
        a_series_4000 = Folder.get_by_id(self.a_series_4000.pk)
        a_series_5000 = Folder.get_by_id(self.a_series_5000.pk)
        a_series_6000 = Folder.get_by_id(self.a_series_6000.pk)
        a_series_7000 = Folder.get_by_id(self.a_series_7000.pk)
        rtx = Folder.get_by_id(self.rtx.pk)
        ti_rtx = Folder.get_by_id(self.ti_rtx.pk)
        n_gpu_2060_ti = Folder.get_by_id(self.n_gpu_2060_ti.pk)
        n_gpu_3070_ti = Folder.get_by_id(self.n_gpu_3070_ti.pk)
        n_gpu_1070_ti = Folder.get_by_id(self.n_gpu_1070_ti.pk)
        n_gpu_1080_ti = Folder.get_by_id(self.n_gpu_1080_ti.pk)
        n_gpu_2060 = Folder.get_by_id(self.n_gpu_2060.pk)
        n_gpu_2070 = Folder.get_by_id(self.n_gpu_2070.pk)
        n_gpu_2080 = Folder.get_by_id(self.n_gpu_2080.pk)
        n_gpu_3080 = Folder.get_by_id(self.n_gpu_3080.pk)
        n_gpu_3060 = Folder.get_by_id(self.n_gpu_3060.pk)
        n_gpu_3070 = Folder.get_by_id(self.n_gpu_3070.pk)
        gtx = Folder.get_by_id(self.gtx.pk)
        ti_gtx = Folder.get_by_id(self.ti_gtx.pk)
        n_gpu_1030 = Folder.get_by_id(self.n_gpu_1030.pk)
        n_gpu_1650 = Folder.get_by_id(self.n_gpu_1650.pk)
        n_gpu_1080 = Folder.get_by_id(self.n_gpu_1080.pk)
        n_gpu_1060 = Folder.get_by_id(self.n_gpu_1060.pk)
        n_gpu_3090 = Folder.get_by_id(self.n_gpu_3090.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(gpu.is_active)
        self.assertTrue(nvidia.is_active)
        self.assertTrue(n_series_1000.is_active)
        self.assertTrue(n_series_2000.is_active)
        self.assertTrue(n_series_3000.is_active)
        self.assertTrue(n_series_4000.is_active)
        self.assertTrue(g_amd.is_active)
        self.assertTrue(a_series_4000.is_active)
        self.assertTrue(a_series_5000.is_active)
        self.assertTrue(a_series_6000.is_active)
        self.assertTrue(a_series_7000.is_active)
        self.assertTrue(rtx.is_active)
        self.assertTrue(ti_rtx.is_active)
        self.assertTrue(n_gpu_2060_ti.is_active)
        self.assertTrue(n_gpu_3070_ti.is_active)
        self.assertTrue(n_gpu_1070_ti.is_active)
        self.assertTrue(n_gpu_1080_ti.is_active)
        self.assertTrue(n_gpu_2060.is_active)
        self.assertTrue(n_gpu_2070.is_active)
        self.assertTrue(n_gpu_2080.is_active)
        self.assertTrue(n_gpu_3080.is_active)
        self.assertTrue(n_gpu_3060.is_active)
        self.assertTrue(n_gpu_3070.is_active)
        self.assertTrue(gtx.is_active)
        self.assertTrue(ti_gtx.is_active)
        self.assertTrue(n_gpu_1030.is_active)
        self.assertTrue(n_gpu_1650.is_active)
        self.assertTrue(n_gpu_1080.is_active)
        self.assertTrue(n_gpu_1060.is_active)
        self.assertTrue(n_gpu_3090.is_active)


