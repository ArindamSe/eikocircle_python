# Generated by Django 4.1.7 on 2023-04-25 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_brands_created_at_brands_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
