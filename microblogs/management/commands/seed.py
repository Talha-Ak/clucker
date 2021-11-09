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
            first_name= self.faker.first_name()
            last_name=self.faker.last_name()
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=f"@seed-{first_name}{last_name}",
                email=f"{first_name}.{last_name}@example.org",
                bio=self.faker.sentence(),
                password="Password123",
            )
        print('Generated 100 users.')
