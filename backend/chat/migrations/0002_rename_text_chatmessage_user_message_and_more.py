# Generated by Django 5.2.1 on 2025-05-14 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessage',
            old_name='text',
            new_name='user_message',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='sender',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='bot_reply',
            field=models.TextField(default='Default reply'),
        ),
    ]
