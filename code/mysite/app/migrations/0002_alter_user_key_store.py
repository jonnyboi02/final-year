# Generated by Django 4.1.3 on 2023-02-17 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='key_store',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]