# Generated by Django 4.2.18 on 2025-02-18 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_post_author"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="image",
        ),
    ]
