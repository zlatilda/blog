# Generated by Django 2.2.1 on 2019-05-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='thumb',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
