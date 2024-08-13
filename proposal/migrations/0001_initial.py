# Generated by Django 5.0 on 2024-04-05 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobposting', '0001_initial'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('status', models.CharField(default='applied', max_length=30)),
                ('accepted_at', models.CharField(max_length=100, null=True)),
                ('paymethod', models.CharField(max_length=10, null=True)),
                ('amountPayed', models.IntegerField(null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobreqjob', to='jobposting.jobrequirement')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobreqworker', to='registration.user')),
            ],
        ),
    ]
