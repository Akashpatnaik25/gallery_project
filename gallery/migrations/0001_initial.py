# Generated by Django 5.1.6 on 2025-02-07 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('image_type', models.CharField(choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')], max_length=10)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
    ]
