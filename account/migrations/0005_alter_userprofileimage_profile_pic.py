# Generated by Django 4.2.1 on 2023-07-31 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_userprofileimage_public_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileimage',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='userimage/'),
        ),
    ]
