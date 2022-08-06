from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder
from apps.directories.test.test_crud import FolderCRUDAPITest

import os.path

URL_MOVE_FOLDER = 'directories:folders-move-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderMoveTest(FolderCRUDAPITest):

    def test_01_move_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'folders_to_move': [self.storage.pk],
            'new_parent_folder': self.n_series_2000.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.get(url_move_folder, payload)
        response_2 = self.client.delete(url_move_folder, payload)
        response_3 = self.client.put(url_move_folder, payload)
        response_4 = self.client.patch(url_move_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_move_folder_missing_field(self):
        """ Testing the validation of required new_parent_folder field """

        payload = {}

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_03_move_folder_not_exists_parent_folder(self):
        """ Testing the validation of required new parent folder exists """

        payload = {
            'folders_to_move': [self.storage.pk],
            'new_parent_folder': 1000
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_04_move_folder_not_exists_the_move_folder(self):
        """ Testing the validation of required the folder to move exists """

        payload = {
            'folders_to_move': [self.storage.pk, 1500],
            'new_parent_folder': [self.n_series_2000.pk]
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_05_move_folder_not_actual_parent_folder_different_of_new_parent_folder(self):
        """ Testing the validation of precondition:
         new parent folder must be different of actual parent folder """

        payload = {
            'folders_to_move': [self.n_series_2000.pk],
            'new_parent_folder': self.nvidia.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_06_move_folder_not_actual_folder_different_of_new_parent_folder(self):
        """ Testing the validation of precondition:
         new parent folder must be different of actual folder """

        payload = {
            'folders_to_move': [self.storage.pk],
            'new_parent_folder': self.storage.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_07_move_folder_not_different_name_folder_children(self):
        """ Testing the validation of precondition:
         the actual folder must to have a different name of the children folders
         in th new parent folder """

        payload = {
            'folders_to_move': [self.n_series_4000.pk],
            'new_parent_folder': self.g_amd.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_08_move_folder_without_children(self):
        """ Testing to move a folder without children to another folder
            new structure:
                ...
                |- Storage
                    |- HDD
                    |- SSD
                ...
                |- Peripherals
                    |- Keyboard
                    |- Mouse
                    |- Headphones
                    |- USB
        """

        payload = {
            'folders_to_move': [self.usb.pk],
            'new_parent_folder': self.peripherals.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.peripherals.pk)
        folder_usb_moved = Folder.get_by_id(self.usb.pk)
        media_path = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{folder_usb_moved.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_usb_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_usb_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(folder_usb_moved.is_child_of(new_parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path))

    def test_09_move_many_folder_without_children(self):
        """ Testing to move many folder without children to another folder
            new structure:
                ...
                |- RTX
                    |- TI
                        |- 2060 TI
                        |- 3070 TI
                |- GTX
                    |- TI
                        |- 1070 TI
                        |- 1080 TI
                ...
        """

        payload = {
            'folders_to_move': [self.n_gpu_1070_ti.pk,
                                self.n_gpu_1080_ti.pk],
            'new_parent_folder': self.ti_gtx.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.ti_gtx.pk)
        folder_1070_moved = Folder.get_by_id(self.n_gpu_1070_ti.pk)
        folder_1080_moved = Folder.get_by_id(self.n_gpu_1080_ti.pk)
        media_path_1070 = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{folder_1070_moved.name}'
        media_path_1080 = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{folder_1080_moved.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_1070_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_1070_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        self.assertEqual(folder_1080_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_1080_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(folder_1070_moved.is_child_of(new_parent_folder))
        self.assertTrue(folder_1080_moved.is_child_of(new_parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_1070))
        self.assertTrue(os.path.exists(media_path_1080))

    def test_10_move_folder_with_children(self):
        """ Testing to move a folder with children to another folder
            new structure:
                ...
                |- Budget
                    |- Peripherals
                        |- Keyboard
                        |- Mouse
                        |- Headphones
        """

        payload = {
            'folders_to_move': [self.peripherals.pk],
            'new_parent_folder': self.budget.pk

        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.budget.pk)
        folder_peripherals_moved = Folder.get_by_id(self.peripherals.pk)
        folder_keyboard_moved = Folder.get_by_id(self.keyboard.pk)
        folder_mouse_moved = Folder.get_by_id(self.mouse.pk)
        folder_headphones_moved = Folder.get_by_id(self.headphones.pk)

        media_path_new_parent_folder = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}'
        media_path_peripherals_moved = f'{media_path_new_parent_folder}/{folder_peripherals_moved.name}'
        media_path_keyboard = f'{media_path_peripherals_moved}/{folder_keyboard_moved.name}'
        media_path_mouse = f'{media_path_peripherals_moved}/{folder_mouse_moved.name}'
        media_path_headphones = f'{media_path_peripherals_moved}/{folder_headphones_moved.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_peripherals_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_peripherals_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(folder_peripherals_moved.is_child_of(new_parent_folder))
        self.assertTrue(folder_keyboard_moved.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_mouse_moved.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_headphones_moved.is_descendant_of(new_parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_peripherals_moved))
        self.assertTrue(os.path.exists(media_path_keyboard))
        self.assertTrue(os.path.exists(media_path_mouse))
        self.assertTrue(os.path.exists(media_path_headphones))

    def test_11_move_many_folder_with_children(self):
        """ Testing to move many folder with children to another folder
            new structure:
                ...
                |- NVIDIA
                    |- Series 1000
                    |- Series 2000
                    |- Series 3000
                    |- Series 4000
                    |- RTX
                        |- TI
                            |- 2060 TI
                            |- 3070 TI
                        |- 2060
                        |- 2070
                        |- 2080
                        |- 3080
                        |- 3060
                        |- 3070
                    |- GTX
                        |- TI
                            |- 1070 TI
                            |- 1080 TI
                        |- 1030
                        |- 1650
                        |- 1080
                        |- 1060
                        |- 3090
                ...
        """

        payload = {
            'folders_to_move': [self.rtx.pk,
                                self.gtx.pk],
            'new_parent_folder': self.nvidia.pk

        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.nvidia.pk)
        folder_rtx_moved = Folder.get_by_id(self.rtx.pk)
        folder_gtx_moved = Folder.get_by_id(self.gtx.pk)

        folder_rtx_ti = Folder.get_by_id(self.ti_rtx.pk)
        folder_gpu_rtx_2080_moved = Folder.get_by_id(self.n_gpu_2080.pk)
        folder_gpu_rtx_3070_ti_moved = Folder.get_by_id(self.n_gpu_3070_ti.pk)

        folder_gtx_ti = Folder.get_by_id(self.ti_gtx.pk)
        folder_gpu_gtx_1070_ti_moved = Folder.get_by_id(self.n_gpu_1070_ti.pk)
        folder_gpu_gtx_1650_moved = Folder.get_by_id(self.n_gpu_1650.pk)

        media_path_new_parent_folder = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}'

        media_path_rtx_moved = f'{media_path_new_parent_folder}/{folder_rtx_moved.name}'
        media_path_rtx_2080_moved = f'{media_path_rtx_moved}/{folder_gpu_rtx_2080_moved.name}'
        media_path_rtx_it_moved = f'{media_path_rtx_moved}/{folder_rtx_ti.name}'
        media_path_rtx_3070_it_moved = f'{media_path_rtx_it_moved}/{folder_gpu_rtx_3070_ti_moved.name}'

        media_path_gtx_moved = f'{media_path_new_parent_folder}/{folder_gtx_moved.name}'
        media_path_gtx_1650_moved = f'{media_path_gtx_moved}/{folder_gpu_gtx_1650_moved.name}'
        media_path_gtx_it_moved = f'{media_path_gtx_moved}/{folder_gtx_ti.name}'
        media_path_gtx_1070_ti_moved = f'{media_path_gtx_it_moved}/{folder_gpu_gtx_1070_ti_moved.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_rtx_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_rtx_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        self.assertEqual(folder_gtx_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_gtx_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(folder_rtx_moved.is_child_of(new_parent_folder))
        self.assertTrue(folder_gtx_moved.is_child_of(new_parent_folder))
        self.assertTrue(folder_rtx_ti.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_gpu_rtx_2080_moved.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_gpu_rtx_3070_ti_moved.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_gtx_ti.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_gpu_gtx_1070_ti_moved.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_gpu_gtx_1650_moved.is_descendant_of(new_parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_rtx_moved))
        self.assertTrue(os.path.exists(media_path_rtx_2080_moved))
        self.assertTrue(os.path.exists(media_path_rtx_it_moved))
        self.assertTrue(os.path.exists(media_path_rtx_3070_it_moved))
        self.assertTrue(os.path.exists(media_path_gtx_moved))
        self.assertTrue(os.path.exists(media_path_gtx_1650_moved))
        self.assertTrue(os.path.exists(media_path_gtx_it_moved))
        self.assertTrue(os.path.exists(media_path_gtx_1070_ti_moved))
