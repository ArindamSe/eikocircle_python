# Generated by Django 4.1.7 on 2023-05-12 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brand_product', '0001_initial'),
        ('awareness_plan', '0006_alter_awarenessplan_medium'),
    ]

    operations = [
        migrations.AddField(
            model_name='awarenessplan',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brand_product.brand_product'),
        ),
    ]
