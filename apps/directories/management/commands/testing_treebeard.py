from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Testing treebeard library'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Successfully testing'))
