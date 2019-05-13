# Generated by Django 2.2.1 on 2019-05-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190512_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='poll',
            new_name='post',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='document',
            field=models.ImageField(default='default.png', upload_to='profile_image'),
        ),
    ]
