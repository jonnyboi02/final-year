# Generated by Django 4.1.3 on 2023-01-30 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_user_private_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='NFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_address', models.TextField(max_length=255)),
                ('collateral', models.FileField(upload_to='collateral')),
            ],
        ),
    ]