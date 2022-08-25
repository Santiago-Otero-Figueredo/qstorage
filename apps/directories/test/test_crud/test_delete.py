from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder
from apps.directories.test.test_crud import FolderCRUDAPITest

import os.path

URL_DELETE_FOLDER = 'directories:folders-delete-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FolderCRUDAPITest):

    def test_01_delete_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'folders_to_delete': [self.hardware.pk]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_move_folder, payload)
        response_2 = self.client.get(url_move_folder, payload)
        response_3 = self.client.put(url_move_folder, payload)
        response_4 = self.client.patch(url_move_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_delete_folder_not_exists(self):
        """ Testing no list folder if does not exists """

        payload = {
            'folders_to_delete': [1000]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_03_not_allow_delete_root_folder(self):
        """ Testing that the root folder can't be deleted even by the owner """

        payload = {
            'folders_to_delete': [self.root_folder.pk]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_04_delete_folder_missing_field(self):
        """ Testing the validation of required folders_to_delete field """

        payload = {}

        url_move_folder = reverse(URL_DELETE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_05_delete_leaf_folder(self):
        """ Testing the delete of leaf folder """

        payload = {
            'folders_to_delete': [self.operative_system.pk]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)

        media_path_folder = f'{settings.MEDIA_ROOT_TEST}{self.operative_system.get_path_folder()}'

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder, payload)

        folder_deleted = Folder.get_by_id(self.operative_system.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(folder_deleted)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_folder))

    def test_06_delete_parent_folder(self):
        """ Testing the delete folder and children """

        payload = {
            'folders_to_delete': [self.cpu.pk]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)

        media_path_cpu_folder = f'{settings.MEDIA_ROOT_TEST}{self.cpu.get_path_folder()}'
        media_path_intel_folder = f'{settings.MEDIA_ROOT_TEST}{self.intel.get_path_folder()}'
        media_path_i5_folder = f'{settings.MEDIA_ROOT_TEST}{self.i5.get_path_folder()}'
        media_path_i3_folder = f'{settings.MEDIA_ROOT_TEST}{self.i3.get_path_folder()}'
        media_path_i7_folder = f'{settings.MEDIA_ROOT_TEST}{self.i7.get_path_folder()}'
        media_path_c_amd_folder = f'{settings.MEDIA_ROOT_TEST}{self.c_amd.get_path_folder()}'
        media_path_r_2600_folder = f'{settings.MEDIA_ROOT_TEST}{self.r_2600.get_path_folder()}'
        media_path_r_3600_folder = f'{settings.MEDIA_ROOT_TEST}{self.r_3600.get_path_folder()}'
        media_path_r_3700_folder = f'{settings.MEDIA_ROOT_TEST}{self.r_3700.get_path_folder()}'

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder, payload)

        cpu_deleted = Folder.get_by_id(self.cpu.pk)
        intel_deleted = Folder.get_by_id(self.intel.pk)
        i5_deleted = Folder.get_by_id(self.i5.pk)
        i3_deleted = Folder.get_by_id(self.i3.pk)
        i7_deleted = Folder.get_by_id(self.i7.pk)
        c_amd_deleted = Folder.get_by_id(self.c_amd.pk)
        r_2600_deleted = Folder.get_by_id(self.r_2600.pk)
        r_3600_deleted = Folder.get_by_id(self.r_3600.pk)
        r_3700_deleted = Folder.get_by_id(self.r_3700.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(cpu_deleted)
        self.assertIsNone(intel_deleted)
        self.assertIsNone(i5_deleted)
        self.assertIsNone(i3_deleted)
        self.assertIsNone(i7_deleted)
        self.assertIsNone(c_amd_deleted)
        self.assertIsNone(r_2600_deleted)
        self.assertIsNone(r_3600_deleted)
        self.assertIsNone(r_3700_deleted)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_cpu_folder))
        self.assertFalse(os.path.exists(media_path_intel_folder))
        self.assertFalse(os.path.exists(media_path_i5_folder))
        self.assertFalse(os.path.exists(media_path_i3_folder))
        self.assertFalse(os.path.exists(media_path_i7_folder))
        self.assertFalse(os.path.exists(media_path_c_amd_folder))
        self.assertFalse(os.path.exists(media_path_r_2600_folder))
        self.assertFalse(os.path.exists(media_path_r_3600_folder))
        self.assertFalse(os.path.exists(media_path_r_3700_folder))

    def test_07_delete_many_leaf_folder(self):
        """ Testing the delete of many leaf folders """

        payload = {
            'folders_to_delete': [self.keyboard.pk,
                                  self.mouse.pk,
                                  self.headphones.pk,
                                  self.budget.pk]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)

        media_path_keyboard_folder = f'{settings.MEDIA_ROOT_TEST}{self.keyboard.get_path_folder()}'
        media_path_mouse_folder = f'{settings.MEDIA_ROOT_TEST}{self.mouse.get_path_folder()}'
        media_path_headphones_folder = f'{settings.MEDIA_ROOT_TEST}{self.headphones.get_path_folder()}'
        media_path_budget_folder = f'{settings.MEDIA_ROOT_TEST}{self.budget.get_path_folder()}'

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder, payload)

        keyboard_deleted = Folder.get_by_id(self.keyboard.pk)
        mouse_deleted = Folder.get_by_id(self.mouse.pk)
        headphones_deleted = Folder.get_by_id(self.headphones.pk)
        budget_deleted = Folder.get_by_id(self.budget.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(keyboard_deleted)
        self.assertIsNone(mouse_deleted)
        self.assertIsNone(headphones_deleted)
        self.assertIsNone(budget_deleted)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_keyboard_folder))
        self.assertFalse(os.path.exists(media_path_mouse_folder))
        self.assertFalse(os.path.exists(media_path_headphones_folder))
        self.assertFalse(os.path.exists(media_path_budget_folder))

    def test_08_delete_many_parent_folder(self):
        """ Testing the delete folder and children """

        payload = {
            'folders_to_delete': [self.nvidia.pk,
                                  self.g_amd.pk,
                                  self.rtx.pk,
                                  self.gtx.pk]
        }

        url_move_folder = reverse(URL_DELETE_FOLDER)

        media_path_nvidia_folder = f'{settings.MEDIA_ROOT_TEST}{self.nvidia.get_path_folder()}'
        media_path_g_amd_folder = f'{settings.MEDIA_ROOT_TEST}{self.g_amd.get_path_folder()}'
        media_path_rtx_folder = f'{settings.MEDIA_ROOT_TEST}{self.rtx.get_path_folder()}'
        media_path_gtx_folder = f'{settings.MEDIA_ROOT_TEST}{self.gtx.get_path_folder()}'

        media_path_n_series_1000_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_series_1000.get_path_folder()}'
        media_path_n_series_2000_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_series_2000.get_path_folder()}'
        media_path_n_series_3000_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_series_3000.get_path_folder()}'
        media_path_n_series_4000_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_series_4000.get_path_folder()}'
        media_path_a_series_4000_folder = f'{settings.MEDIA_ROOT_TEST}{self.a_series_4000.get_path_folder()}'
        media_path_a_series_5000_folder = f'{settings.MEDIA_ROOT_TEST}{self.a_series_5000.get_path_folder()}'
        media_path_a_series_6000_folder = f'{settings.MEDIA_ROOT_TEST}{self.a_series_6000.get_path_folder()}'
        media_path_a_series_7000_folder = f'{settings.MEDIA_ROOT_TEST}{self.a_series_7000.get_path_folder()}'
        media_path_ti_rtx_folder = f'{settings.MEDIA_ROOT_TEST}{self.ti_rtx.get_path_folder()}'
        media_path_n_gpu_2060_ti_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_2060_ti.get_path_folder()}'
        media_path_n_gpu_3070_ti_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_3070_ti.get_path_folder()}'
        media_path_n_gpu_1070_ti_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_1070_ti.get_path_folder()}'
        media_path_n_gpu_1080_ti_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_1080_ti.get_path_folder()}'
        media_path_n_gpu_2060_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_2060.get_path_folder()}'
        media_path_n_gpu_2070_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_2070.get_path_folder()}'
        media_path_n_gpu_2080_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_2080.get_path_folder()}'
        media_path_n_gpu_3080_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_3080.get_path_folder()}'
        media_path_n_gpu_3060_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_3060.get_path_folder()}'
        media_path_n_gpu_3070_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_3070.get_path_folder()}'
        media_path_ti_gtx_folder = f'{settings.MEDIA_ROOT_TEST}{self.ti_gtx.get_path_folder()}'
        media_path_n_gpu_1030_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_1030.get_path_folder()}'
        media_path_n_gpu_1650_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_1650.get_path_folder()}'
        media_path_n_gpu_1080_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_1080.get_path_folder()}'
        media_path_n_gpu_1060_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_1060.get_path_folder()}'
        media_path_n_gpu_3090_folder = f'{settings.MEDIA_ROOT_TEST}{self.n_gpu_3090.get_path_folder()}'

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder, payload)

        nvidia_deleted = Folder.get_by_id(self.nvidia.pk)
        g_amd_deleted = Folder.get_by_id(self.g_amd.pk)
        rtx_deleted = Folder.get_by_id(self.rtx.pk)
        gtx_deleted = Folder.get_by_id(self.gtx.pk)

        n_series_1000_delete = Folder.get_by_id(self.n_series_1000.pk)
        n_series_2000_delete = Folder.get_by_id(self.n_series_2000.pk)
        n_series_3000_delete = Folder.get_by_id(self.n_series_3000.pk)
        n_series_4000_delete = Folder.get_by_id(self.n_series_4000.pk)
        a_series_4000_delete = Folder.get_by_id(self.a_series_4000.pk)
        a_series_5000_delete = Folder.get_by_id(self.a_series_5000.pk)
        a_series_6000_delete = Folder.get_by_id(self.a_series_6000.pk)
        a_series_7000_delete = Folder.get_by_id(self.a_series_7000.pk)
        ti_rtx_delete = Folder.get_by_id(self.ti_rtx.pk)
        n_gpu_2060_ti_delete = Folder.get_by_id(self.n_gpu_2060_ti.pk)
        n_gpu_3070_ti_delete = Folder.get_by_id(self.n_gpu_3070_ti.pk)
        n_gpu_1070_ti_delete = Folder.get_by_id(self.n_gpu_1070_ti.pk)
        n_gpu_1080_ti_delete = Folder.get_by_id(self.n_gpu_1080_ti.pk)
        n_gpu_2060_delete = Folder.get_by_id(self.n_gpu_2060.pk)
        n_gpu_2070_delete = Folder.get_by_id(self.n_gpu_2070.pk)
        n_gpu_2080_delete = Folder.get_by_id(self.n_gpu_2080.pk)
        n_gpu_3080_delete = Folder.get_by_id(self.n_gpu_3080.pk)
        n_gpu_3060_delete = Folder.get_by_id(self.n_gpu_3060.pk)
        n_gpu_3070_delete = Folder.get_by_id(self.n_gpu_3070.pk)
        ti_gtx_delete = Folder.get_by_id(self.ti_gtx.pk)
        n_gpu_1030_delete = Folder.get_by_id(self.n_gpu_1030.pk)
        n_gpu_1650_delete = Folder.get_by_id(self.n_gpu_1650.pk)
        n_gpu_1080_delete = Folder.get_by_id(self.n_gpu_1080.pk)
        n_gpu_1060_delete = Folder.get_by_id(self.n_gpu_1060.pk)
        n_gpu_3090_delete = Folder.get_by_id(self.n_gpu_3090.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(nvidia_deleted)
        self.assertIsNone(g_amd_deleted)
        self.assertIsNone(rtx_deleted)
        self.assertIsNone(gtx_deleted)
        self.assertIsNone(n_series_1000_delete)
        self.assertIsNone(n_series_2000_delete)
        self.assertIsNone(n_series_3000_delete)
        self.assertIsNone(n_series_4000_delete)
        self.assertIsNone(a_series_4000_delete)
        self.assertIsNone(a_series_5000_delete)
        self.assertIsNone(a_series_6000_delete)
        self.assertIsNone(a_series_7000_delete)
        self.assertIsNone(ti_rtx_delete)
        self.assertIsNone(n_gpu_2060_ti_delete)
        self.assertIsNone(n_gpu_3070_ti_delete)
        self.assertIsNone(n_gpu_1070_ti_delete)
        self.assertIsNone(n_gpu_1080_ti_delete)
        self.assertIsNone(n_gpu_2060_delete)
        self.assertIsNone(n_gpu_2070_delete)
        self.assertIsNone(n_gpu_2080_delete)
        self.assertIsNone(n_gpu_3080_delete)
        self.assertIsNone(n_gpu_3060_delete)
        self.assertIsNone(n_gpu_3070_delete)
        self.assertIsNone(ti_gtx_delete)
        self.assertIsNone(n_gpu_1030_delete)
        self.assertIsNone(n_gpu_1650_delete)
        self.assertIsNone(n_gpu_1080_delete)
        self.assertIsNone(n_gpu_1060_delete)
        self.assertIsNone(n_gpu_3090_delete)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_nvidia_folder))
        self.assertFalse(os.path.exists(media_path_g_amd_folder))
        self.assertFalse(os.path.exists(media_path_rtx_folder))
        self.assertFalse(os.path.exists(media_path_gtx_folder))
        self.assertFalse(os.path.exists(media_path_n_series_1000_folder))
        self.assertFalse(os.path.exists(media_path_n_series_2000_folder))
        self.assertFalse(os.path.exists(media_path_n_series_3000_folder))
        self.assertFalse(os.path.exists(media_path_n_series_4000_folder))
        self.assertFalse(os.path.exists(media_path_a_series_4000_folder))
        self.assertFalse(os.path.exists(media_path_a_series_5000_folder))
        self.assertFalse(os.path.exists(media_path_a_series_6000_folder))
        self.assertFalse(os.path.exists(media_path_a_series_7000_folder))
        self.assertFalse(os.path.exists(media_path_ti_rtx_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_2060_ti_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_3070_ti_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_1070_ti_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_1080_ti_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_2060_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_2070_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_2080_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_3080_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_3060_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_3070_folder))
        self.assertFalse(os.path.exists(media_path_ti_gtx_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_1030_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_1650_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_1080_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_1060_folder))
        self.assertFalse(os.path.exists(media_path_n_gpu_3090_folder))
