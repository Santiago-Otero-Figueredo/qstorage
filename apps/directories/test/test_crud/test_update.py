from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder

from apps.directories.test.test_crud import FolderCRUDAPITest

import os.path

URL_DETAIL_FOLDER = 'directories:folders-detail'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderUpdateTest(FolderCRUDAPITest):

    def test_01_update_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'name': 'update_name',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.g_amd.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.put(url_detail_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_update_folder_not_exists(self):
        """ Testing not update folder if does not exists """

        payload = {
            'name': 'update_name',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': 1000})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_detail_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_update_root_name_not_allow(self):
        """ Testing the permissions for update the root folder action.
        The user can not modify this folder even if he is the owner """

        update_data = {
            'name': 'update_name'
        }

        url_update_folders = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.root_folder.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_update_folders, update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_04_update_name_leaf_folder_in_root(self):
        """ Testing the update name and the update of paths of the leaf folder in root
            new structure:
                |- / (root)
                    |- Hardware
                        ...
                    |- OP
        """

        update_data = {
            'name': 'OP',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.operative_system.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        parent_folder = Folder.objects.get(pk=self.root_folder.pk)
        child_folder = Folder.objects.get(pk=self.operative_system.pk)

        media_path_new_folder = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/{child_folder.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(child_folder.name, 'OP')
        self.assertEqual(child_folder.get_path_parent_folder(), parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(child_folder.is_child_of(parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_folder))

    def test_05_update_name_leaf_folder_in_parent(self):
        """ Testing the update name and the update of paths of the leaf folder in a parent folder
            new structure:
                |- Hardware
                    ...
                    |- Budget 2022
        """

        update_data = {
            'name': 'Budget 2022',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.budget.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        parent_folder = Folder.objects.get(pk=self.hardware.pk)
        child_folder = Folder.objects.get(pk=self.budget.pk)

        media_path_new_folder = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/{child_folder.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(child_folder.name, 'Budget 2022')
        self.assertEqual(child_folder.get_path_parent_folder(), parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(child_folder.is_child_of(parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_folder))

    def test_06_update_name_child_folder_in_parent(self):
        """ Testing the update name and the update of paths of the children folders in
            children folder of a parent folder.
            new structure:
                |- Hardware
                    ...
                    |- Gaming assets
        """

        update_data = {
            'name': 'Gaming assets',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.peripherals.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        parent_folder = Folder.objects.get(pk=self.hardware.pk)
        peripherals_folder = Folder.objects.get(pk=self.peripherals.pk)

        keyboard_folder = Folder.objects.get(pk=self.keyboard.pk)
        mouse_folder = Folder.objects.get(pk=self.mouse.pk)
        headphones_folder = Folder.objects.get(pk=self.headphones.pk)

        media_path_parent_folder = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/{peripherals_folder.name}'
        media_path_keyboard_folder = f'{media_path_parent_folder}/{keyboard_folder.name}'
        media_path_mouse_folder = f'{media_path_parent_folder}/{mouse_folder.name}'
        media_path_headphones_folder = f'{media_path_parent_folder}/{headphones_folder.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(peripherals_folder.name, 'Gaming assets')
        self.assertEqual(peripherals_folder.get_path_parent_folder(), parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(peripherals_folder.is_child_of(parent_folder))
        self.assertTrue(keyboard_folder.is_child_of(peripherals_folder))
        self.assertTrue(mouse_folder.is_child_of(peripherals_folder))
        self.assertTrue(headphones_folder.is_child_of(peripherals_folder))
        self.assertTrue(keyboard_folder.is_descendant_of(parent_folder))
        self.assertTrue(mouse_folder.is_descendant_of(parent_folder))
        self.assertTrue(headphones_folder.is_descendant_of(parent_folder))
        # Validation of folders update name in media folder
        self.assertTrue(os.path.exists(media_path_parent_folder))
        self.assertTrue(os.path.exists(media_path_keyboard_folder))
        self.assertTrue(os.path.exists(media_path_mouse_folder))
        self.assertTrue(os.path.exists(media_path_headphones_folder))

    def test_07_update_name_parent_folder(self):
        """ Testing the update name and the update of paths of the children folders in
            parent folder of a many folder
            new structure:
                |- Hardware
                    ...
                    |- Graphics cards
                        |- NVIDIA
                           ...
                        |- AMD
                            ...
                        |- RTX
                            |- TI
                                ...
                            ...
                        |- GTX
                            ...
        """

        update_data = {
            'name': 'Graphics cards',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.gpu.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        parent_folder = Folder.objects.get(pk=self.hardware.pk)
        gpu_folder = Folder.objects.get(pk=self.gpu.pk)

        nvidia_folder = Folder.objects.get(pk=self.nvidia.pk)
        g_amd_folder = Folder.objects.get(pk=self.g_amd.pk)
        rtx_folder = Folder.objects.get(pk=self.rtx.pk)
        gtx_folder = Folder.objects.get(pk=self.gtx.pk)

        ti_rtx_folder = Folder.objects.get(pk=self.ti_rtx.pk)
        n_gpu_3070_ti_folder = Folder.objects.get(pk=self.n_gpu_3070_ti.pk)
        n_gpu_1650_folder = Folder.objects.get(pk=self.n_gpu_1650.pk)
        a_series_4000 = Folder.objects.get(pk=self.a_series_4000.pk)
        n_series_2000 = Folder.objects.get(pk=self.n_series_2000.pk)

        media_path_parent_folder = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/{gpu_folder.name}'
        media_path_nvidia = f'{media_path_parent_folder}/{nvidia_folder.name}'
        media_path_amd = f'{media_path_parent_folder}/{g_amd_folder.name}'
        media_path_rtx = f'{media_path_parent_folder}/{rtx_folder.name}'
        media_path_gtx = f'{media_path_parent_folder}/{gtx_folder.name}'
        media_path_1650 = f'{media_path_gtx}/{n_gpu_1650_folder.name}'
        media_path_rtx_ti = f'{media_path_rtx}/{ti_rtx_folder.name}'
        media_pth_3070_ti = f'{media_path_rtx_ti}/{n_gpu_3070_ti_folder.name}'
        media_pth_2000 = f'{media_path_nvidia}/{n_series_2000.name}'
        media_pth_4000 = f'{media_path_amd}/{a_series_4000.name}'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(gpu_folder.name, 'Graphics cards')
        self.assertEqual(gpu_folder.get_path_parent_folder(), parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(gpu_folder.is_child_of(parent_folder))
        self.assertTrue(nvidia_folder.is_child_of(gpu_folder))
        self.assertTrue(g_amd_folder.is_child_of(gpu_folder))
        self.assertTrue(rtx_folder.is_child_of(gpu_folder))
        self.assertTrue(gtx_folder.is_child_of(gpu_folder))
        self.assertTrue(ti_rtx_folder.is_descendant_of(parent_folder))
        self.assertTrue(n_gpu_3070_ti_folder.is_descendant_of(parent_folder))
        self.assertTrue(n_gpu_1650_folder.is_descendant_of(parent_folder))
        self.assertTrue(a_series_4000.is_descendant_of(parent_folder))
        self.assertTrue(n_series_2000.is_descendant_of(parent_folder))
        # Validation of folders update name in media folder
        self.assertTrue(os.path.exists(media_path_parent_folder))
        self.assertTrue(os.path.exists(media_path_nvidia))
        self.assertTrue(os.path.exists(media_path_amd))
        self.assertTrue(os.path.exists(media_path_rtx))
        self.assertTrue(os.path.exists(media_path_gtx))
        self.assertTrue(os.path.exists(media_path_1650))
        self.assertTrue(os.path.exists(media_path_rtx_ti))
        self.assertTrue(os.path.exists(media_pth_3070_ti))
        self.assertTrue(os.path.exists(media_pth_2000))
        self.assertTrue(os.path.exists(media_pth_4000))
