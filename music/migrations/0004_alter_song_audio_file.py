# Generated by Django 4.2.4 on 2023-09-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_remove_song_duration_song_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default='default_audio.mp3', upload_to='songs/%y'),
        ),
    ]