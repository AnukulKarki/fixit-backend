# Generated by Django 5.0 on 2024-04-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gighire', '0004_alter_gigproposal_paymethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gigproposal',
            name='paymethod',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
