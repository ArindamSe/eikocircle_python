# Generated by Django 4.1.7 on 2023-04-25 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_address_user_company_name_user_mobile_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='brand_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.brands'),
        ),
    ]
