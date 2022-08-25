from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import File
from apps.directories.test.files.test_crud import FileCRUDAPITest

import os.path

URL_DELETE_FILES = 'directories:files-delete-file'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FileCRUDAPITest):

    def test_01_delete_file_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'files_to_delete': [self.f_windows.pk]
        }

        url_move_folder = reverse(URL_DELETE_FILES)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_move_folder, payload)
        response_2 = self.client.get(url_move_folder, payload)
        response_3 = self.client.put(url_move_folder, payload)
        response_4 = self.client.patch(url_move_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_delete_file_not_exists(self):
        """ Testing no delete file if does not exists """

        payload = {
            'files_to_delete': [1000]
        }

        url_move_folder = reverse(URL_DELETE_FILES)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_03_delete_file_missing_field(self):
        """ Testing the validation of required files_to_delete field """

        payload = {}

        url_move_folder = reverse(URL_DELETE_FILES)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_delete_files_in_leaf_folder(self):
        """ Testing the delete of files in leaf folder """

        payload = {
            'files_to_delete': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_DELETE_FILES)

        f_windows_deleted = File.get_by_id(self.f_windows.pk)
        f_linux_deleted = File.get_by_id(self.f_linux.pk)

        media_path_windows = f_windows_deleted.get_full_path()
        media_path_linux = f_linux_deleted.get_full_path()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder, payload)

        f_windows_deleted = File.get_by_id(self.f_windows.pk)
        f_linux_deleted = File.get_by_id(self.f_linux.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(f_windows_deleted)
        self.assertIsNone(f_linux_deleted)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_windows))
        self.assertFalse(os.path.exists(media_path_linux))

    def test_07_delete_parent_folder(self):
        """ Testing the delete folder and children """

        payload = {
            'files_to_delete': [self.f_budget.pk,
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

        url_move_folder = reverse(URL_DELETE_FILES)

        f_budget_delete = File.get_by_id(self.f_budget.pk)
        f_hdd_delete = File.get_by_id(self.f_hdd.pk)
        f_mv_2_delete = File.get_by_id(self.f_mv_2.pk)
        f_series_1000_delete = File.get_by_id(self.f_series_1000.pk)
        f_series_2000_delete = File.get_by_id(self.f_series_2000.pk)
        f_series_4000_delete = File.get_by_id(self.f_series_4000.pk)
        f_series_5000_delete = File.get_by_id(self.f_series_5000.pk)
        f_1070_ti_delete = File.get_by_id(self.f_1070_ti.pk)
        f_1080_ti_delete = File.get_by_id(self.f_1080_ti.pk)
        f_2060_ti_delete = File.get_by_id(self.f_2060_ti.pk)
        f_3060_ti_delete = File.get_by_id(self.f_3060_ti.pk)
        f_1030_delete = File.get_by_id(self.f_1030.pk)

        media_path_f_budget = f_budget_delete.get_full_path()
        media_path_f_hdd = f_hdd_delete.get_full_path()
        media_path_f_mv_2 = f_mv_2_delete.get_full_path()
        media_path_f_series_1000 = f_series_1000_delete.get_full_path()
        media_path_f_series_2000 = f_series_2000_delete.get_full_path()
        media_path_f_series_4000 = f_series_4000_delete.get_full_path()
        media_path_f_series_5000 = f_series_5000_delete.get_full_path()
        media_path_f_1070_ti = f_1070_ti_delete.get_full_path()
        media_path_f_1080_ti = f_1080_ti_delete.get_full_path()
        media_path_f_2060_ti = f_2060_ti_delete.get_full_path()
        media_path_f_3060_ti = f_3060_ti_delete.get_full_path()
        media_path_f_1030 = f_1030_delete.get_full_path()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder, payload)

        f_budget_delete = File.get_by_id(self.f_budget.pk)
        f_hdd_delete = File.get_by_id(self.f_hdd.pk)
        f_mv_2_delete = File.get_by_id(self.f_mv_2.pk)
        f_series_1000_delete = File.get_by_id(self.f_series_1000.pk)
        f_series_2000_delete = File.get_by_id(self.f_series_2000.pk)
        f_series_4000_delete = File.get_by_id(self.f_series_4000.pk)
        f_series_5000_delete = File.get_by_id(self.f_series_5000.pk)
        f_1070_ti_delete = File.get_by_id(self.f_1070_ti.pk)
        f_1080_ti_delete = File.get_by_id(self.f_1080_ti.pk)
        f_2060_ti_delete = File.get_by_id(self.f_2060_ti.pk)
        f_3060_ti_delete = File.get_by_id(self.f_3060_ti.pk)
        f_1030_delete = File.get_by_id(self.f_1030.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(f_budget_delete)
        self.assertIsNone(f_hdd_delete)
        self.assertIsNone(f_mv_2_delete)
        self.assertIsNone(f_series_1000_delete)
        self.assertIsNone(f_series_2000_delete)
        self.assertIsNone(f_series_4000_delete)
        self.assertIsNone(f_series_5000_delete)
        self.assertIsNone(f_1070_ti_delete)
        self.assertIsNone(f_1080_ti_delete)
        self.assertIsNone(f_2060_ti_delete)
        self.assertIsNone(f_3060_ti_delete)
        self.assertIsNone(f_1030_delete)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_f_budget))
        self.assertFalse(os.path.exists(media_path_f_hdd))
        self.assertFalse(os.path.exists(media_path_f_mv_2))
        self.assertFalse(os.path.exists(media_path_f_series_1000))
        self.assertFalse(os.path.exists(media_path_f_series_2000))
        self.assertFalse(os.path.exists(media_path_f_series_4000))
        self.assertFalse(os.path.exists(media_path_f_series_5000))
        self.assertFalse(os.path.exists(media_path_f_1070_ti))
        self.assertFalse(os.path.exists(media_path_f_1080_ti))
        self.assertFalse(os.path.exists(media_path_f_2060_ti))
        self.assertFalse(os.path.exists(media_path_f_3060_ti))
        self.assertFalse(os.path.exists(media_path_f_1030))
