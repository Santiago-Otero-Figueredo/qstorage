from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import override_settings

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.directories.models import Folder

from shutil import rmtree

URL_MOVE_FOLDER = 'directories:folders-move-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderCRUDAPITest(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initial structure of directories for the testing
            |- / (root)
                |- Hardware
                    |- Storage
                        |- HDD
                        |- SSD
                        |- USB
                    |- Memories
                        |- RAM
                        |- MV2
                    |- GPU
                        |- NVIDIA
                            |- Series 1000
                            |- Series 2000
                            |- Series 3000
                            |- Series 4000
                        |- AMD
                            |- Series 4000
                            |- Series 5000
                            |- Series 6000
                            |- Series 7000
                        |- RTX
                            |- TI
                                |- 2060 TI
                                |- 3070 TI
                                |- 1070 TI
                                |- 1080 TI
                            |- 2060
                            |- 2070
                            |- 2080
                            |- 3080
                            |- 3060
                            |- 3070
                        |- GTX
                            |- TI
                            |- 1030
                            |- 1650
                            |- 1080
                            |- 1060
                            |- 3090
                    |- CPU
                        |- Intel
                            |- i5
                            |- i3
                            |- i7
                        |- AMD
                            |- R2600
                            |- R3600
                            |- R3700
                    |- Peripherals
                        |- Keyboard
                        |- Mouse
                        |- Headphones
                    |- Budget
                |- Operative system
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

        cls.hardware = Folder.create_folder_and_assign_to_parent(cls.user, 'Hardware', cls.root_folder) # ROOT
        cls.storage = Folder.create_folder_and_assign_to_parent(cls.user, 'Storage', cls.hardware) # hardware
        cls.hdd = Folder.create_folder_and_assign_to_parent(cls.user, 'HDD', cls.storage) # storage
        cls.ssd = Folder.create_folder_and_assign_to_parent(cls.user, 'SSD', cls.storage) # storage
        cls.usb = Folder.create_folder_and_assign_to_parent(cls.user, 'USB', cls.storage) # storage

        cls.memories = Folder.create_folder_and_assign_to_parent(cls.user, 'Memories', cls.hardware) # hardware
        cls.ram = Folder.create_folder_and_assign_to_parent(cls.user, 'RAM', cls.memories) # memories
        cls.mv2 = Folder.create_folder_and_assign_to_parent(cls.user, 'MV2', cls.memories) # memories

        cls.gpu = Folder.create_folder_and_assign_to_parent(cls.user, 'GPU', cls.hardware) # hardware
        cls.nvidia = Folder.create_folder_and_assign_to_parent(cls.user, 'NVIDIA', cls.gpu) # GPU
        cls.n_series_1000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 1000', cls.nvidia) # NVIDIA
        cls.n_series_2000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 2000', cls.nvidia) # NVIDIA
        cls.n_series_3000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 3000', cls.nvidia) # NVIDIA
        cls.n_series_4000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 4000', cls.nvidia) # NVIDIA

        cls.g_amd = Folder.create_folder_and_assign_to_parent(cls.user, 'AMD', cls.gpu) # GPU
        cls.a_series_4000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 4000', cls.g_amd) # AMD
        cls.a_series_5000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 5000', cls.g_amd) # AMD
        cls.a_series_6000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 6000', cls.g_amd) # AMD
        cls.a_series_7000 = Folder.create_folder_and_assign_to_parent(cls.user, 'Series 7000', cls.g_amd) # AMD

        cls.rtx = Folder.create_folder_and_assign_to_parent(cls.user, 'RTX', cls.gpu) # GPU
        cls.ti_rtx = Folder.create_folder_and_assign_to_parent(cls.user, 'TI', cls.rtx) # RTX

        cls.n_gpu_2060_ti = Folder.create_folder_and_assign_to_parent(cls.user, '2060 TI', cls.ti_rtx) # TI
        cls.n_gpu_3070_ti = Folder.create_folder_and_assign_to_parent(cls.user, '3070 TI', cls.ti_rtx) # TI
        cls.n_gpu_1070_ti = Folder.create_folder_and_assign_to_parent(cls.user, '1070 TI', cls.ti_rtx) # TI
        cls.n_gpu_1080_ti = Folder.create_folder_and_assign_to_parent(cls.user, '1080 TI', cls.ti_rtx) # TI

        cls.n_gpu_2060 = Folder.create_folder_and_assign_to_parent(cls.user, '2060',  cls.rtx) # RTX
        cls.n_gpu_2070 = Folder.create_folder_and_assign_to_parent(cls.user, '2070',  cls.rtx) # RTX
        cls.n_gpu_2080 = Folder.create_folder_and_assign_to_parent(cls.user, '2080',  cls.rtx) # RTX
        cls.n_gpu_3080 = Folder.create_folder_and_assign_to_parent(cls.user, '3080',  cls.rtx) # RTX
        cls.n_gpu_3060 = Folder.create_folder_and_assign_to_parent(cls.user, '3060',  cls.rtx) # RTX
        cls.n_gpu_3070 = Folder.create_folder_and_assign_to_parent(cls.user, '3070',  cls.rtx) # RTX

        cls.gtx = Folder.create_folder_and_assign_to_parent(cls.user, 'GTX', cls.gpu) # GPU
        cls.ti_gtx = Folder.create_folder_and_assign_to_parent(cls.user, 'TI', cls.gtx) # GTX
        cls.n_gpu_1030 = Folder.create_folder_and_assign_to_parent(cls.user, '1030', cls.gtx) # GTX
        cls.n_gpu_1650 = Folder.create_folder_and_assign_to_parent(cls.user, '1650', cls.gtx) # GTX
        cls.n_gpu_1080 = Folder.create_folder_and_assign_to_parent(cls.user, '1080', cls.gtx) # GTX
        cls.n_gpu_1060 = Folder.create_folder_and_assign_to_parent(cls.user, '1060', cls.gtx) # GTX
        cls.n_gpu_3090 = Folder.create_folder_and_assign_to_parent(cls.user, '3090', cls.gtx) # GTX

        cls.cpu = Folder.create_folder_and_assign_to_parent(cls.user, 'CPU', cls.hardware) # hardware
        cls.intel = Folder.create_folder_and_assign_to_parent(cls.user, 'Intel', cls.cpu) # CPU
        cls.i5 = Folder.create_folder_and_assign_to_parent(cls.user, 'i5', cls.intel) # intel
        cls.i3 = Folder.create_folder_and_assign_to_parent(cls.user, 'i3', cls.intel) # intel
        cls.i7 = Folder.create_folder_and_assign_to_parent(cls.user, 'i7', cls.intel) # intel

        cls.c_amd = Folder.create_folder_and_assign_to_parent(cls.user, 'AMD', cls.cpu ) # CPU
        cls.r_2600 = Folder.create_folder_and_assign_to_parent(cls.user, 'R2600', cls.c_amd) # AMD
        cls.r_3600 = Folder.create_folder_and_assign_to_parent(cls.user, 'R3600', cls.c_amd) # AMD
        cls.r_3700 = Folder.create_folder_and_assign_to_parent(cls.user, 'R3700', cls.c_amd) # AMD

        cls.peripherals = Folder.create_folder_and_assign_to_parent(cls.user, 'Peripherals', cls.hardware) # hardware
        cls.keyboard = Folder.create_folder_and_assign_to_parent(cls.user, 'Keyboard', cls.peripherals) # Peripherals
        cls.mouse = Folder.create_folder_and_assign_to_parent(cls.user, 'Mouse', cls.peripherals) # Peripherals
        cls.headphones = Folder.create_folder_and_assign_to_parent(cls.user, 'Headphones', cls.peripherals) # Peripherals

        cls.budget = Folder.create_folder_and_assign_to_parent(cls.user, 'Budget', cls.hardware) # hardware

        cls.operative_system = Folder.create_folder_and_assign_to_parent(cls.user, 'Operative system', cls.root_folder) # ROOT


    @classmethod
    def tearDownClass(cls):
        """ Remove the test file in media"""
        super(FolderCRUDAPITest, cls).tearDownClass()
        rmtree(settings.MEDIA_ROOT_TEST, ignore_errors=True)