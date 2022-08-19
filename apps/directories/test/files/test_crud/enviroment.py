from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File as FileCore

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import override_settings

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.directories.models import Folder, File

from shutil import rmtree

URL_MOVE_FOLDER = 'directories:folders-move-folder'


def upload_file_temporally(name_file):
    path = f'{settings.DATOS_INICIALES}/test_files/'
    data = FileCore(open(f'{path}/{name_file}', 'rb'))
    upload_file = SimpleUploadedFile(name_file, data.read(), content_type='multipart/form-data')
    return upload_file


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FileCRUDAPITest(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initial structure of directories for the testing
            |- / (root)
                |- Hardware
                    |- Storage
                        |- HDD.png
                        |- MV_2.png
                    |- GPU
                        |- NVIDIA
                            |- Series_1000.pdf
                            |- Series_2000.pdf
                        |- AMD
                            |- Series 4000.pdf
                            |- Series 5000.pdf
                        |- RTX
                            |- TI
                                |- 2060 TI.png
                                |- 3070 TI.png
                                |- 1070 TI.png
                                |- 1080 TI.png
                            |- 2060.jpg
                        |- GTX
                            |- TI
                            |- 1030.pdf
                    |- Peripherals
                        |- Keyboard.png
                        |- Mouse.png
                        |- Headphones.png
                    |- Budget.csv
                |- Windows.pdf
                |- linux.pdf
        """
        super(FileCRUDAPITest, cls).setUpClass()
        cls.user = get_user_model().objects.create(
            pk=10,
            first_name='file test',
            last_name='testing',
            username='TFT',
            email='testing_files@xyz.com',
            password='contrasenia@123456'
        )

        cls.token, _ = Token.objects.get_or_create(user=cls.user)
        cls.root_folder = Folder.get_root_folder_by_user(cls.user)

        cls.f_windows = File.objects.create(parent_folder=cls.root_folder, file=upload_file_temporally('Windows.pdf'))  # F ROOT
        cls.f_linux = File.objects.create(parent_folder=cls.root_folder, file=upload_file_temporally('linux.pdf'))  # F ROOT

        cls.hardware = Folder.create_folder_and_assign_to_parent(cls.user, 'Hardware', cls.root_folder)  # ROOT

        cls.f_budget = File.objects.create(parent_folder=cls.hardware, file=upload_file_temporally('Budget.csv'))  # F Hardware

        cls.storage = Folder.create_folder_and_assign_to_parent(cls.user, 'Storage', cls.hardware)  # Hardware

        cls.f_hdd = File.objects.create(parent_folder=cls.storage, file=upload_file_temporally('HDD.png'))  # F Storage
        cls.f_mv_2 = File.objects.create(parent_folder=cls.storage, file=upload_file_temporally('MV_2.png'))  # F Storage

        cls.gpu = Folder.create_folder_and_assign_to_parent(cls.user, 'GPU', cls.hardware)  # Hardware
        cls.nvidia = Folder.create_folder_and_assign_to_parent(cls.user, 'NVIDIA', cls.gpu)  # GPU

        cls.f_series_1000 = File.objects.create(parent_folder=cls.nvidia, file=upload_file_temporally('Series_1000.pdf'))  # F NVIDIA
        cls.f_series_2000 = File.objects.create(parent_folder=cls.nvidia, file=upload_file_temporally('Series_2000.pdf'))  # F NVIDIA

        cls.g_amd = Folder.create_folder_and_assign_to_parent(cls.user, 'AMD', cls.gpu)  # GPU

        cls.f_series_4000 = File.objects.create(parent_folder=cls.g_amd, file=upload_file_temporally('Series 4000.pdf'))  # F AMD
        cls.f_series_5000 = File.objects.create(parent_folder=cls.g_amd, file=upload_file_temporally('Series 5000.pdf'))  # F AMD

        cls.rtx = Folder.create_folder_and_assign_to_parent(cls.user, 'RTX', cls.gpu)  # GPU
        cls.ti_rtx = Folder.create_folder_and_assign_to_parent(cls.user, 'TI', cls.rtx)  # RTX

        cls.f_1070_TI = File.objects.create(parent_folder=cls.ti_rtx, file=upload_file_temporally('1070 TI.png'))  # F TI
        cls.f_1080_TI = File.objects.create(parent_folder=cls.ti_rtx, file=upload_file_temporally('1080 TI.png'))  # F TI
        cls.f_2060_TI = File.objects.create(parent_folder=cls.ti_rtx, file=upload_file_temporally('2060 TI.png'))  # F TI
        cls.f_3060_TI = File.objects.create(parent_folder=cls.ti_rtx, file=upload_file_temporally('3060 TI.png'))  # F TI

        cls.gtx = Folder.create_folder_and_assign_to_parent(cls.user, 'GTX', cls.gpu)  # GPU
        cls.ti_gtx = Folder.create_folder_and_assign_to_parent(cls.user, 'TI', cls.gtx)  # GTX

        cls.f_1030 = File.objects.create(parent_folder=cls.gtx, file=upload_file_temporally('1030.pdf'))  # F GTX

        cls.peripherals = Folder.create_folder_and_assign_to_parent(cls.user, 'Peripherals', cls.hardware)  # Hardware

        cls.f_keyboard = File.objects.create(
            parent_folder=cls.peripherals,
            file=upload_file_temporally('Keyboard.png')
        )  # F Peripherals
        cls.f_mouse = File.objects.create(
            parent_folder=cls.peripherals,
            file=upload_file_temporally('Mouse.png')
        )  # F Peripherals
        cls.f_headphones = File.objects.create(
            parent_folder=cls.peripherals,
            file=upload_file_temporally('Headphones.png')
        )  # F Peripherals

    @classmethod
    def tearDownClass(cls):
        """ Remove the test file in media"""
        super(FileCRUDAPITest, cls).tearDownClass()
        rmtree(settings.MEDIA_ROOT_TEST, ignore_errors=True)
