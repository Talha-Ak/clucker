from django.core.management.base import BaseCommand, CommandError
from microblogs.models import User
from faker import Faker

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    # Generate 100 random users
    def handle(self, *args, **options):
        for i in range(0, 100):
            User.objects.create_user(
                username='@seed-' + self.faker.user_name(),
                first_name= self.faker.first_name(),
                last_name=self.faker.last_name(),
                email=self.faker.email(),
                bio=self.faker.sentence(),
            )
        print('Generated 100 users.')
