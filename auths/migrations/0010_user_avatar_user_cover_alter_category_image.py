# Generated by Django 4.2 on 2023-04-14 00:17

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):
    dependencies = [
        ("auths", "0009_remove_category_category_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=easy_thumbnails.fields.ThumbnailerImageField(
                blank=True, null=True, upload_to="users_avatar", verbose_name="avatar"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="cover",
            field=easy_thumbnails.fields.ThumbnailerImageField(
                blank=True, null=True, upload_to="users_cover", verbose_name="cover"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=easy_thumbnails.fields.ThumbnailerImageField(
                blank=True, null=True, upload_to="category_images", verbose_name="image"
            ),
        ),
    ]
