# Generated by Django 4.1.7 on 2023-05-02 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_center', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectioncenter',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
