# Generated by Django 4.2 on 2023-04-13 22:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auths", "0005_taggeduser_user_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="taggeduser",
            old_name="user",
            new_name="content_object",
        ),
    ]
