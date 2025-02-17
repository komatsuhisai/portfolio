# Generated by Django 4.2.6 on 2024-01-02 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_character_closed_mouth_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='body_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/body/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='closed_eyes_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/eyes/closed/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='closed_mouth_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/mouth/closed/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='half_open_mouth_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/mouth/half_open/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='open_eyes_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/eyes/open/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='open_mouth_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/mouth/open/'),
        ),
    ]
