from django.core.management.base import BaseCommand, CommandError
from microblogs.models import User

class Command(BaseCommand):

    # Remove generated users
    def handle(self, *args, **options):
        User.objects.filter(username__startswith='@seed-').delete()
        print('Removed generated users.')
