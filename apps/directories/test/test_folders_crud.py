from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.directories.models import Folder

from shutil import rmtree

import os.path

URL_CREATE_FOLDER = 'directories:folders-create-folder'
URL_LIST_CHILDREN = 'directories:folders-children-folders'
URL_DETAIL_FOLDER = 'directories:folders-detail'
URL_MOVE_FOLDER = 'directories:folders-move-folder'
URL_MOVE_TO_RECICLE_BIN = 'directories:folders-move-to-recycle-bin'
URL_RECOVER_FOLDER = 'directories:folders-recover-folder'
URL_DELETE_FOLDER = 'directories:folders-delete-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderCRUDAPITest(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initial structure of directories for the testing
            |- / (root)
                |- test_1_nested_1
                |- test_1
                    |- test_1_nested
                        |- test_1_nested_1
                        |- test_1_nested_2
                            |- test_2_nested_1_nested
                    |- test_2_nested
                |- test_2
                |- test_folder_move
                    |- test_folder_move_1
                    |- test_folder_move_2
                    |- test_folder_move_3
                |- test_leaf_folder
                |- test_new_folder_parent
                |- test_update_folder
                    |- test_update_nested_1
                        |- child_1_update_1
                        |- child_2_update_1
                    |- test_update_nested_2
                        |- child_1_update_2
                            |- child_1_update_2_nested
                    |- test_update_nested_3
                |- delete_folder
                    |- delete_folder_children_1
                        |- delete_folder_children_1_nested
                    |- delete_folder_children_2
        """
        super(FolderCRUDAPITest, cls).setUpClass()
        cls.user = get_user_model().objects.create(
            pk=1,
            first_name='test',
            last_name='testing',
            username='TT',
            email='testing@xyz.com',
            password='contrasenia@123456'
        )

        cls.token, _ = Token.objects.get_or_create(user=cls.user)
        cls.root_folder = Folder.get_root_folder_by_user(cls.user)
        cls.delete_folder = cls.root_folder.add_child(owner_user=cls.user, name='delete_folder', route='/')
        cls.delete_folder_children_1 = cls.delete_folder.add_child(
            owner_user=cls.user,
            name='delete_folder_children_1',
            route='/'
        )
        cls.delete_folder_children_2 = cls.delete_folder.add_child(
            owner_user=cls.user,
            name='delete_folder_children_2',
            route='/'
        )
        cls.delete_folder_children_1_nested = cls.delete_folder_children_1.add_child(
            owner_user=cls.user,
            name='delete_folder_children_1_nested',
            route='/'
        )

        cls.test_same_name = cls.root_folder.add_child(owner_user=cls.user, name='test_1_nested_1', route='/')

        cls.test_folder = cls.root_folder.add_child(owner_user=cls.user, name='test_1', route='/')

        cls.test_2_folder = cls.root_folder.add_child(owner_user=cls.user, name='test_2', route='/')
        cls.test_folder_move = cls.root_folder.add_child(owner_user=cls.user, name='test_folder_move', route='/')
        cls.leaf_folder = cls.root_folder.add_child(owner_user=cls.user, name='test_leaf_folder', route='/')
        cls.test_new_folder_parent = cls.root_folder.add_child(
            owner_user=cls.user,
            name='test_new_folder_parent',
            route='/'
        )
        cls.test_update_folder = cls.root_folder.add_child(owner_user=cls.user, name='test_update_folder', route='/')

        cls.nested_test_1_folder_1 = cls.test_folder.add_child(owner_user=cls.user, name='test_1_nested', route='/')
        cls.test_folder.add_child(owner_user=cls.user, name='test_2_nested', route='/')

        cls.nested_test_folder_1 = cls.nested_test_1_folder_1.add_child(
            owner_user=cls.user,
            name='test_1_nested_1',
            route='/'
        )
        cls.nested_test_folder_2 = cls.nested_test_1_folder_1.add_child(
            owner_user=cls.user,
            name='test_2_nested_2',
            route='/'
        )
        cls.nested_test_folder_2_nested = cls.nested_test_folder_2.add_child(
            owner_user=cls.user,
            name='test_2_nested_1_nested',
            route='/'
        )

        cls.test_folder_move_1 = cls.test_folder_move.add_child(
            owner_user=cls.user,
            name='test_folder_move_1',
            route='/'
        )
        cls.test_folder_move_2 = cls.test_folder_move.add_child(
            owner_user=cls.user,
            name='test_folder_move_2',
            route='/'
        )
        cls.test_folder_move_3 = cls.test_folder_move.add_child(
            owner_user=cls.user,
            name='test_folder_move_3',
            route='/'
        )

        cls.test_update_nested_1 = cls.test_update_folder.add_child(
            owner_user=cls.user,
            name='test_update_nested_1',
            route='/'
        )
        cls.test_update_nested_2 = cls.test_update_folder.add_child(
            owner_user=cls.user,
            name='test_update_nested_2',
            route='/'
        )
        cls.test_update_nested_3 = cls.test_update_folder.add_child(
            owner_user=cls.user,
            name='test_update_nested_3',
            route='/'
        )

        cls.child_1_update_1 = cls.test_update_nested_1.add_child(
            owner_user=cls.user,
            name='child_1_update_1',
            route='/'
        )
        cls.child_2_update_1 = cls.test_update_nested_1.add_child(
            owner_user=cls.user,
            name='child_2_update_1',
            route='/'
        )

        cls.child_1_update_2 = cls.test_update_nested_2.add_child(
            owner_user=cls.user,
            name='child_1_update_2',
            route='/'
        )
        cls.child_1_child_1_update_2 = cls.child_1_update_2.add_child(
            owner_user=cls.user,
            name='child_1_update_2_nested',
            route='/'
        )

    def test_create_folder_in_root(self):
        """ Testing the creation of a folder in the root folder """
        payload = {
            'name': 'folder_test',
            'owner_user': self.user.pk
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url_create_folder, payload)

        child_folder = Folder.objects.get(name='folder_test')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(child_folder.is_child_of(self.root_folder))

    def test_create_folder_in_child_folder(self):
        """ Testing the creation of a folder inside another folder other than root folder """
        payload = {
            'name': 'folder_test_nested',
            'owner_user': self.user.pk
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_create_folder, payload)

        child_folder = Folder.objects.get(name='folder_test_nested')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(child_folder.is_child_of(self.test_folder))
        self.assertEqual(child_folder.route, '1/test_1/')

    def test_update_name_file(self):
        """ Testing the update name and the update of paths of the children folders """

        update_data = {
            'name': 'update_name',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        child_folder = Folder.get_by_id(self.test_folder.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(child_folder.name, 'update_name')
        self.assertEqual(child_folder.route, '1/')
        self.assertTrue(child_folder.is_child_of(self.root_folder))

    def test_update_name_leaf_folder_in_root(self):
        """ Testing the update name and the update of paths of the leaf folder in root """

        update_data = {
            'name': 'update_name_leaf',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.leaf_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)
        leaf_folder_update = Folder.get_by_id(self.leaf_folder.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(leaf_folder_update.name, 'update_name_leaf')
        self.assertEqual(leaf_folder_update.route, '1/')
        self.assertTrue(leaf_folder_update.is_child_of(self.root_folder))

    def test_update_name_leaf_folder_in_parent(self):
        """ Testing the update name and the update of paths of the leaf folder in a parent folder """

        update_data = {
            'name': 'update_name_leaf_folder',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.test_update_nested_3.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)
        folder_update = Folder.get_by_id(self.test_update_nested_3.pk)

        media_path_parent_folder = f'{settings.MEDIA_ROOT_TEST}{self.test_update_folder.get_path_folder()}'
        media_path_folder = f'{media_path_parent_folder}/{folder_update.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_update.name, 'update_name_leaf_folder')
        self.assertEqual(folder_update.route, '1/test_update_folder/')
        # Validation of changes in inheritance database
        self.assertTrue(folder_update.is_child_of(self.test_update_folder))
        # Validation of folders update name in media folder
        self.assertTrue(os.path.exists(media_path_folder))

    def test_update_name_child_folder_in_parent(self):
        """ Testing the update name and the update of paths of the children folders in
        children folder of a parent folder"""

        update_data = {
            'name': 'update_name_child_folder',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.child_1_update_2.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)
        folder_update = Folder.get_by_id(self.child_1_update_2.pk)

        child_folder_update = Folder.get_by_id(self.child_1_child_1_update_2.pk)

        media_path_parent_folder = f'{settings.MEDIA_ROOT_TEST}{self.test_update_nested_2.get_path_folder()}'
        media_path_folder_update = f'{media_path_parent_folder}/{folder_update.name}'

        media_path_child_folder = f'{media_path_folder_update}/{child_folder_update.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_update.name, 'update_name_child_folder')
        self.assertEqual(folder_update.route, '1/test_update_folder/test_update_nested_2/')
        # Validation of changes in inheritance database
        self.assertTrue(folder_update.is_child_of(self.test_update_nested_2))
        self.assertTrue(child_folder_update.is_child_of(folder_update))
        # Validation of folders update name in media folder
        self.assertTrue(os.path.exists(media_path_folder_update))
        self.assertTrue(os.path.exists(media_path_child_folder))

    def test_update_name_parent_folder(self):
        """ Testing the update name and the update of paths of the children folders in
        parent folder of a many folder"""

        update_data = {
            'name': 'update_name_parent_folder',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.test_update_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)
        folder_update = Folder.get_by_id(self.test_update_folder.pk)

        child_folder_update_1 = Folder.get_by_id(self.test_update_nested_1.pk)
        child_folder_update_2 = Folder.get_by_id(self.test_update_nested_2.pk)
        nested_child_update_2 = Folder.get_by_id(self.child_1_child_1_update_2.pk)

        media_path_parent_folder = f'{settings.MEDIA_ROOT_TEST}{self.root_folder.get_path_folder()}'
        media_path_folder_update = f'{media_path_parent_folder}/{folder_update.name}'

        media_path_update_1 = f'{media_path_folder_update}/{child_folder_update_1.name}'
        media_path_update_2 = f'{media_path_folder_update}/{child_folder_update_2.name}'
        media_nested_child_update_2 = f'{media_path_update_2}/update_name_child_folder/{nested_child_update_2.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_update.name, 'update_name_parent_folder')
        self.assertEqual(folder_update.route, '1/')
        # Validation of changes in inheritance database
        self.assertTrue(folder_update.is_child_of(self.root_folder))
        self.assertTrue(child_folder_update_1.is_child_of(self.test_update_folder))
        self.assertTrue(child_folder_update_2.is_child_of(self.test_update_folder))
        self.assertTrue(nested_child_update_2.is_descendant_of(self.test_update_folder))
        # Validation of folders update name in media folder
        self.assertTrue(os.path.exists(media_path_folder_update))
        self.assertTrue(os.path.exists(media_path_update_1))
        self.assertTrue(os.path.exists(media_path_update_2))
        self.assertTrue(os.path.exists(media_nested_child_update_2))

    def test_no_exists_pk_folder(self):
        """ Testing a pk folder that does not exists """

        url_list_children = reverse(URL_LIST_CHILDREN, kwargs={'pk': 100})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url_list_children)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_children_folders_in_root(self):
        """ Testing the list of children folders in root """

        url_list_children = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_children)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'delete_folder')
        self.assertEqual(response.data[1]['name'], 'test_1')
        self.assertEqual(response.data[2]['name'], 'test_1_nested_1')
        self.assertEqual(response.data[3]['name'], 'test_2')
        self.assertEqual(response.data[4]['name'], 'test_folder_move')
        self.assertEqual(response.data[5]['name'], 'test_leaf_folder')
        self.assertEqual(response.data[6]['name'], 'test_new_folder_parent')
        self.assertEqual(response.data[7]['name'], 'test_update_folder')

    def test_list_children_folders_in_nested_folder(self):
        """ Testing the list of children folders in another folder different of root """

        url_list_children = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_children)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'test_1_nested')
        self.assertEqual(response.data[1]['name'], 'test_2_nested')

    def test_move_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'new_parent_folder': self.test_folder_move.pk
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.test_folder_move_3.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.get(url_move_folder, payload)
        response_2 = self.client.delete(url_move_folder, payload)
        response_3 = self.client.put(url_move_folder, payload)
        response_4 = self.client.patch(url_move_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_move_folder_missing_field(self):
        """ Testing the validation of required new_parent_folder field """

        payload = {}

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.test_folder_move_3.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_folder_not_exists_folder(self):
        """ Testing the validation of required new parent folder exists """

        payload = {
            'new_parent_folder': 1000
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.test_folder_move_3.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_move_folder_not_actual_parent_folder_different_of_new_parent_folder(self):
        """ Testing the validation of precondition:
         new parent folder must be different of actual parent folder """

        payload = {
            'new_parent_folder': self.test_folder_move.pk
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.test_folder_move_3.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_move_folder_not_actual_folder_different_of_new_parent_folder(self):
        """ Testing the validation of precondition:
         new parent folder must be different of actual folder """

        payload = {
            'new_parent_folder': self.test_folder_move_3.pk
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.test_folder_move_3.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_move_folder_not_different_name_folder_children(self):
        """ Testing the validation of precondition:
         the actual folder must to have a different name of the children folders
         in th new parent folder """

        payload = {
            'new_parent_folder': self.nested_test_1_folder_1.pk
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.test_same_name.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_move_folder_without_children(self):
        """ Testing to move a folder without children to another folder"""

        payload = {
            'new_parent_folder': self.test_2_folder.pk
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.test_folder_move_3.pk}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        test_folder_moved = Folder.get_by_id(self.test_folder_move_3.pk)
        media_path = f'{settings.MEDIA_ROOT_TEST}{self.test_2_folder.get_path_folder()}/{test_folder_moved.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(test_folder_moved.get_parent().name, self.test_2_folder.name)
        self.assertEqual(test_folder_moved.get_path_parent_folder(), self.test_2_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(test_folder_moved.is_child_of(self.test_2_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path))

    def test_move_folder_with_children(self):
        """ Testing to move a folder with children to another folder"""

        payload = {
            'new_parent_folder': self.test_new_folder_parent.pk
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.nested_test_1_folder_1.pk}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        test_folder_moved = Folder.get_by_id(self.nested_test_1_folder_1.pk)
        nested_test_folder_1_moved = Folder.get_by_id(self.nested_test_folder_1.pk)
        nested_test_folder_2_moved = Folder.get_by_id(self.nested_test_folder_2.pk)
        nested_test_folder_2_nested_moved = Folder.get_by_id(self.nested_test_folder_2_nested.pk)

        media_path_new_parent_folder = f'{settings.MEDIA_ROOT_TEST}{self.test_new_folder_parent.get_path_folder()}'

        media_path_test_folder_moved = f'{media_path_new_parent_folder}/{test_folder_moved.name}'
        media_path_nested_test_folder_1_moved = f'{media_path_test_folder_moved}/{nested_test_folder_1_moved.name}'
        media_path_nested_test_folder_2_moved = f'{media_path_test_folder_moved}/{nested_test_folder_2_moved.name}'
        media_path_children_test_2 = f'{media_path_nested_test_folder_2_moved}/{nested_test_folder_2_nested_moved.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(test_folder_moved.get_parent().name, self.test_new_folder_parent.name)
        self.assertEqual(test_folder_moved.get_path_parent_folder(), self.test_new_folder_parent.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(test_folder_moved.is_child_of(self.test_new_folder_parent))
        self.assertTrue(nested_test_folder_1_moved.is_descendant_of(self.test_new_folder_parent))
        self.assertTrue(nested_test_folder_2_moved.is_descendant_of(self.test_new_folder_parent))
        self.assertTrue(nested_test_folder_2_nested_moved.is_descendant_of(self.test_new_folder_parent))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_test_folder_moved))
        self.assertTrue(os.path.exists(media_path_nested_test_folder_1_moved))
        self.assertTrue(os.path.exists(media_path_nested_test_folder_2_moved))
        self.assertTrue(os.path.exists(media_path_children_test_2))

    def test_move_folder_to_recicle_bin(self):
        """ Testing the disabled folder and children """

        url_move_folder = reverse(
            URL_MOVE_TO_RECICLE_BIN,
            kwargs={'pk': self.test_folder.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder)

        test_parent_folder = Folder.get_by_id(self.test_folder.pk)
        test_1 = Folder.get_by_id(self.nested_test_1_folder_1.pk)
        test_2 = Folder.get_by_id(self.nested_test_folder_2_nested.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(test_parent_folder.is_active)
        self.assertFalse(test_1.is_active)
        self.assertFalse(test_2.is_active)

    def test_recover_folder(self):
        """ Testing the recover folder and children """

        url_move_folder = reverse(
            URL_RECOVER_FOLDER,
            kwargs={'pk': self.test_folder.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder)

        test_parent_folder = Folder.get_by_id(self.test_folder.pk)
        test_1 = Folder.get_by_id(self.nested_test_1_folder_1.pk)
        test_2 = Folder.get_by_id(self.nested_test_folder_2_nested.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(test_parent_folder.is_active)
        self.assertTrue(test_1.is_active)
        self.assertTrue(test_2.is_active)

    def test_delete_folder(self):
        """ Testing the delete folder and children """

        url_move_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': self.delete_folder.pk}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        media_path_test_parent_folder = f'{settings.MEDIA_ROOT_TEST}{self.delete_folder.get_path_folder()}'
        media_path_test_1 = f'{settings.MEDIA_ROOT_TEST}{self.delete_folder_children_1.get_path_folder()}'
        media_path_test_2 = f'{settings.MEDIA_ROOT_TEST}{self.delete_folder_children_2.get_path_folder()}'
        media_path_test_3 = f'{settings.MEDIA_ROOT_TEST}{self.delete_folder_children_1_nested.get_path_folder()}'

        response = self.client.delete(url_move_folder)

        test_parent_folder = Folder.get_by_id(self.delete_folder.pk)
        test_1 = Folder.get_by_id(self.delete_folder_children_1.pk)
        test_2 = Folder.get_by_id(self.delete_folder_children_2.pk)
        test_3 = Folder.get_by_id(self.delete_folder_children_1_nested.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(test_parent_folder)
        self.assertIsNone(test_1)
        self.assertIsNone(test_2)
        self.assertIsNone(test_3)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_test_parent_folder))
        self.assertFalse(os.path.exists(media_path_test_1))
        self.assertFalse(os.path.exists(media_path_test_2))
        self.assertFalse(os.path.exists(media_path_test_3))

    def test_not_allow_delete_root_folder(self):
        """ Testing that the root folder can't be deleted even by the owner """

        url_move_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': self.root_folder.pk}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def tearDownClass(cls):
        """ Remove the test file in media"""
        super(FolderCRUDAPITest, cls).tearDownClass()
        rmtree(settings.MEDIA_ROOT_TEST, ignore_errors=True)
# Create your tests here.
