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

        payload = {
            'folders_to_disable': [self.hardware.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_move_folder, payload)
        response_2 = self.client.get(url_move_folder, payload)
        response_3 = self.client.put(url_move_folder, payload)
        response_4 = self.client.delete(url_move_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_move_recicle_bin_folder_not_exists(self):
        """ Testing no list folder if does not exists """

        payload = {
            'folders_to_disable': [1000]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_03_move_folder_to_recicle_bin_missing_field(self):
        """ Testing the validation of required folders_to_disable field """

        payload = {}

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_recover_folder_missing_field(self):
        """ Testing the validation of required folders_to_recover field """

        payload = {}

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_05_move_leaf_folder_to_recicle_bin(self):
        """ Testing the disabled a leaf folder """

        payload = {
            'folders_to_disable': [self.operative_system.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        folder_moved = Folder.get_by_id(self.operative_system.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(folder_moved.is_active)

    def test_06_move_parent_folder_to_recicle_bin(self):
        """ Testing the disabled a parent folder and his children """

        payload = {
            'folders_to_disable': [self.gpu.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

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

    def test_07_recover_leaf_folder_to_recicle_bin(self):
        """ Testing the recover a leaf folder """

        payload = {
            'folders_to_recover': [self.operative_system.pk]
        }

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        folder_moved = Folder.get_by_id(self.operative_system.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(folder_moved.is_active)

    def test_08_move_parent_folder_to_recicle_bin(self):
        """ Testing the recover a parent folder and his children """

        payload = {
            'folders_to_recover': [self.gpu.pk]
        }

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

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

    def test_09_move_many_leaf_folder_to_recicle_bin(self):
        """ Testing the disabled of many leaf folders """

        payload = {
            'folders_to_disable': [self.operative_system.pk,
                                   self.ram.pk,
                                   self.mv2.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        operative_system_folder_move = Folder.get_by_id(self.operative_system.pk)
        ram_folder_move = Folder.get_by_id(self.ram.pk)
        mv2_folder_move = Folder.get_by_id(self.mv2.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(operative_system_folder_move.is_active)
        self.assertFalse(ram_folder_move.is_active)
        self.assertFalse(mv2_folder_move.is_active)

    def test_10_recover_many_leaf_folder_to_recicle_bin(self):
        """ Testing the recover of many leaf folders """

        payload = {
            'folders_to_recover': [self.operative_system.pk,
                                   self.ram.pk,
                                   self.mv2.pk]
        }

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        operative_system_folder_recover = Folder.get_by_id(self.operative_system.pk)
        ram_folder_recover = Folder.get_by_id(self.ram.pk)
        mv2_folder_recover = Folder.get_by_id(self.mv2.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(operative_system_folder_recover.is_active)
        self.assertTrue(ram_folder_recover.is_active)
        self.assertTrue(mv2_folder_recover.is_active)

    def test_11_move_many_parent_folder_to_recicle_bin(self):
        """ Testing the disabled of many parent folders and his children """

        payload = {
            'folders_to_disable': [self.gpu.pk,
                                   self.cpu.pk,
                                   self.storage.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

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

        cpu = Folder.get_by_id(self.cpu.pk)
        intel = Folder.get_by_id(self.intel.pk)
        i5 = Folder.get_by_id(self.i5.pk)
        i3 = Folder.get_by_id(self.i3.pk)
        i7 = Folder.get_by_id(self.i7.pk)
        c_amd = Folder.get_by_id(self.c_amd.pk)
        r_2600 = Folder.get_by_id(self.r_2600.pk)
        r_3600 = Folder.get_by_id(self.r_3600.pk)
        r_3700 = Folder.get_by_id(self.r_3700.pk)

        storage = Folder.get_by_id(self.storage.pk)
        hdd = Folder.get_by_id(self.hdd.pk)
        ssd = Folder.get_by_id(self.ssd.pk)
        usb = Folder.get_by_id(self.usb.pk)

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

        self.assertFalse(cpu.is_active)
        self.assertFalse(intel.is_active)
        self.assertFalse(i5.is_active)
        self.assertFalse(i3.is_active)
        self.assertFalse(i7.is_active)
        self.assertFalse(c_amd.is_active)
        self.assertFalse(r_2600.is_active)
        self.assertFalse(r_3600.is_active)
        self.assertFalse(r_3700.is_active)

        self.assertFalse(storage.is_active)
        self.assertFalse(hdd.is_active)
        self.assertFalse(ssd.is_active)
        self.assertFalse(usb.is_active)

    def test_12_recover_many_parent_folder_to_recicle_bin(self):
        """ Testing the recover of many parent folders and his children """

        payload = {
            'folders_to_recover': [self.gpu.pk,
                                   self.cpu.pk,
                                   self.storage.pk]
        }

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

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

        cpu = Folder.get_by_id(self.cpu.pk)
        intel = Folder.get_by_id(self.intel.pk)
        i5 = Folder.get_by_id(self.i5.pk)
        i3 = Folder.get_by_id(self.i3.pk)
        i7 = Folder.get_by_id(self.i7.pk)
        c_amd = Folder.get_by_id(self.c_amd.pk)
        r_2600 = Folder.get_by_id(self.r_2600.pk)
        r_3600 = Folder.get_by_id(self.r_3600.pk)
        r_3700 = Folder.get_by_id(self.r_3700.pk)

        storage = Folder.get_by_id(self.storage.pk)
        hdd = Folder.get_by_id(self.hdd.pk)
        ssd = Folder.get_by_id(self.ssd.pk)
        usb = Folder.get_by_id(self.usb.pk)

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

        self.assertTrue(cpu.is_active)
        self.assertTrue(intel.is_active)
        self.assertTrue(i5.is_active)
        self.assertTrue(i3.is_active)
        self.assertTrue(i7.is_active)
        self.assertTrue(c_amd.is_active)
        self.assertTrue(r_2600.is_active)
        self.assertTrue(r_3600.is_active)
        self.assertTrue(r_3700.is_active)

        self.assertTrue(storage.is_active)
        self.assertTrue(hdd.is_active)
        self.assertTrue(ssd.is_active)
        self.assertTrue(usb.is_active)
