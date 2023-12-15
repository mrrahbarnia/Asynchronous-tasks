from time import sleep

from django.core.management import (
    BaseCommand,
    CommandError,
    call_command
)


class Command(BaseCommand):

    help = 'This command will make migrations \
            and migrate automatically each 5 seconds.'
    
    def handle(self, *args, **options):
        call_command('makemigrations')
        sleep(3)
        call_command('migrate')
