# Generated by Django 5.0.1 on 2024-01-11 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_taggit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='taggit',
            new_name='tags',
        ),
    ]
