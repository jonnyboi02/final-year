# Generated by Django 4.1.3 on 2023-04-27 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_negotiation'),
    ]

    operations = [
        migrations.AddField(
            model_name='negotiation',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
