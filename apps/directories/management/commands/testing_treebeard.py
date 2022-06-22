from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from ...models import Folder

from pprint import pprint

class Command(BaseCommand):
    help = 'Testing treebeard library'

    def handle(self, *args, **options):
        
        #try:
        user = get_user_model().objects.get(pk=3)
        #get = lambda node_id: Folder.objects.get(pk=node_id)
        #root = Folder.add_root(owner_user=user,name='Computer Hardware')
        #node = get(root.pk).add_child(owner_user=user, name='Memory')
        #get(node.pk).add_sibling(owner_user=user, name='Hard Drives')
        #get(node.pk).add_sibling(owner_user=user, name='SSD')
        #get(node.pk).add_child(owner_user=user, name='Desktop Memory')
        #get(node.pk).add_child(owner_user=user, name='Laptop Memory')
        #get(node.pk).add_child(owner_user=user, name='Server Memory')
        
        node = Folder.objects.get(owner_user=user, name='Desktop Memory')
        #root = Folder.objects.get_root_folder_by_user(user)
        pprint(Folder.dump_bulk())
        #pprint(root.get_tree())
        pprint(node.get_root_nodes())
        #root.delete()
        #except Exception as e:
        #    raise CommandError(f'Error testing: {e}')

        self.stdout.write(self.style.SUCCESS('Successfully testing'))