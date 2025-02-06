# Generated by Django 4.2.6 on 2024-01-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_character_selected_voice_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='body_image',
            field=models.ImageField(blank=True, default='images/body/body.png', upload_to='images/body/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='closed_eyes_image',
            field=models.ImageField(blank=True, default='images/eyes/closed/eyes_close.png', upload_to='images/eyes/closed/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='closed_mouth_image',
            field=models.ImageField(blank=True, default='images/mouth/closed/mouth.png', upload_to='images/mouth/closed/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='half_open_mouth_image',
            field=models.ImageField(blank=True, default='images/mouth/half_open/mouth_half.png', upload_to='images/mouth/half_open/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='open_eyes_image',
            field=models.ImageField(blank=True, default='images/eyes/open/eyes.png', upload_to='images/eyes/open/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='open_mouth_image',
            field=models.ImageField(blank=True, default='images/mouth/open/mouth_open.png', upload_to='images/mouth/open/'),
        ),
    ]
