# Generated by Django 3.2.7 on 2021-12-01 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblogs', '0003_auto_20211116_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]
