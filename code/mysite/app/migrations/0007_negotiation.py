# Generated by Django 4.1.3 on 2023-04-27 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_loanrequest_request_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Negotiation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.TextField()),
                ('user', models.TextField()),
                ('customer_offer', models.BooleanField(default=False)),
                ('bank_offer', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, upload_to='negotiation_photos')),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]