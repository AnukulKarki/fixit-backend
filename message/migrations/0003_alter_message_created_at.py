# Generated by Django 5.0 on 2024-04-12 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_alter_message_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 12, 20, 53, 17, 31776), null=True),
        ),
    ]
