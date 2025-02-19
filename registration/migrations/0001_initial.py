# Generated by Django 5.0 on 2024-04-05 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('isKycVerified', models.BooleanField(default=False, null=True)),
                ('phone', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('district', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('street_name', models.CharField(max_length=50)),
                ('image', models.ImageField(null=True, upload_to='image/citizenship')),
                ('rating', models.IntegerField(default=0)),
                ('citizenship_no', models.CharField(max_length=50)),
                ('role', models.CharField(default='client', max_length=15)),
                ('profileImg', models.ImageField(null=True, upload_to='image/profile')),
                ('codeVerified', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.user')),
            ],
        ),
    ]
