from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import File
from apps.directories.test.files.test_crud import FileCRUDAPITest

URL_MOVE_TO_RECICLE_BIN = 'directories:files-move-to-recycle-bin'
URL_RECOVER_FOLDER = 'directories:files-recover-files'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FileCRUDAPITest):

    def test_01_move_recicle_bin_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'files_to_disable': [self.f_s_linux.pk]
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

    def test_02_recover_recicle_bin_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'files_to_disable': [self.f_s_linux.pk]
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

    def test_03_move_recicle_bin_folder_not_exists(self):
        """ Testing no recover files if does not exists """

        payload = {
            'files_to_disable': [1000]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_04_move_folder_to_recicle_bin_missing_field(self):
        """ Testing the validation of required files_to_disable field """

        payload = {}

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_05_recover_folder_missing_field(self):
        """ Testing the validation of required files_to_recover field """

        payload = {}

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_06_move_file_in_leaf_folder_to_recicle_bin(self):
        """ Testing the disabled of file in leaf folder """

        payload = {
            'files_to_disable': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        f_windows_disable = File.get_by_id(self.f_windows.pk)
        f_linux_disable = File.get_by_id(self.f_linux.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(f_windows_disable.is_active)
        self.assertFalse(f_linux_disable.is_active)

    def test_07_move_file_in_parent_folder_to_recicle_bin(self):
        """ Testing the disabled of files in parent folder"""

        payload = {
            'files_to_disable': [self.f_budget.pk,
                                self.f_hdd.pk,
                                self.f_mv_2.pk,
                                self.f_series_1000.pk,
                                self.f_series_2000.pk,
                                self.f_series_4000.pk,
                                self.f_series_5000.pk,
                                self.f_1070_ti.pk,
                                self.f_1080_ti.pk,
                                self.f_2060_ti.pk,
                                self.f_3060_ti.pk,
                                self.f_1030.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        f_budget_disable = File.get_by_id(self.f_budget.pk)
        f_hdd_disable = File.get_by_id(self.f_hdd.pk)
        f_mv_2_disable = File.get_by_id(self.f_mv_2.pk)
        f_series_1000_disable = File.get_by_id(self.f_series_1000.pk)
        f_series_2000_disable = File.get_by_id(self.f_series_2000.pk)
        f_series_4000_disable = File.get_by_id(self.f_series_4000.pk)
        f_series_5000_disable = File.get_by_id(self.f_series_5000.pk)
        f_1070_ti_disable = File.get_by_id(self.f_1070_ti.pk)
        f_1080_ti_disable = File.get_by_id(self.f_1080_ti.pk)
        f_2060_ti_disable = File.get_by_id(self.f_2060_ti.pk)
        f_3060_ti_disable = File.get_by_id(self.f_3060_ti.pk)
        f_1030_disable = File.get_by_id(self.f_1030.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(f_budget_disable.is_active)
        self.assertFalse(f_hdd_disable.is_active)
        self.assertFalse(f_mv_2_disable.is_active)
        self.assertFalse(f_series_1000_disable.is_active)
        self.assertFalse(f_series_2000_disable.is_active)
        self.assertFalse(f_series_4000_disable.is_active)
        self.assertFalse(f_series_5000_disable.is_active)
        self.assertFalse(f_1070_ti_disable.is_active)
        self.assertFalse(f_1080_ti_disable.is_active)
        self.assertFalse(f_2060_ti_disable.is_active)
        self.assertFalse(f_3060_ti_disable.is_active)
        self.assertFalse(f_1030_disable.is_active)

    def test_08_recover_files_in_leaf_folder_to_recicle_bin(self):
        """ Testing the recover a file in root folder """

        payload = {
            'files_to_recover': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        f_windows_disable = File.get_by_id(self.f_windows.pk)
        f_linux_disable = File.get_by_id(self.f_linux.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(f_windows_disable.is_active)
        self.assertTrue(f_linux_disable.is_active)

    def test_09_move_parent_folder_to_recicle_bin(self):
        """ Testing the recover of files in parent folder """

        payload = {
            'files_to_recover': [self.f_budget.pk,
                                self.f_hdd.pk,
                                self.f_mv_2.pk,
                                self.f_series_1000.pk,
                                self.f_series_2000.pk,
                                self.f_series_4000.pk,
                                self.f_series_5000.pk,
                                self.f_1070_ti.pk,
                                self.f_1080_ti.pk,
                                self.f_2060_ti.pk,
                                self.f_3060_ti.pk,
                                self.f_1030.pk]
        }

        url_move_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        f_budget_disable = File.get_by_id(self.f_budget.pk)
        f_hdd_disable = File.get_by_id(self.f_hdd.pk)
        f_mv_2_disable = File.get_by_id(self.f_mv_2.pk)
        f_series_1000_disable = File.get_by_id(self.f_series_1000.pk)
        f_series_2000_disable = File.get_by_id(self.f_series_2000.pk)
        f_series_4000_disable = File.get_by_id(self.f_series_4000.pk)
        f_series_5000_disable = File.get_by_id(self.f_series_5000.pk)
        f_1070_ti_disable = File.get_by_id(self.f_1070_ti.pk)
        f_1080_ti_disable = File.get_by_id(self.f_1080_ti.pk)
        f_2060_ti_disable = File.get_by_id(self.f_2060_ti.pk)
        f_3060_ti_disable = File.get_by_id(self.f_3060_ti.pk)
        f_1030_disable = File.get_by_id(self.f_1030.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(f_budget_disable.is_active)
        self.assertTrue(f_hdd_disable.is_active)
        self.assertTrue(f_mv_2_disable.is_active)
        self.assertTrue(f_series_1000_disable.is_active)
        self.assertTrue(f_series_2000_disable.is_active)
        self.assertTrue(f_series_4000_disable.is_active)
        self.assertTrue(f_series_5000_disable.is_active)
        self.assertTrue(f_1070_ti_disable.is_active)
        self.assertTrue(f_1080_ti_disable.is_active)
        self.assertTrue(f_2060_ti_disable.is_active)
        self.assertTrue(f_3060_ti_disable.is_active)
        self.assertTrue(f_1030_disable.is_active)
