# Generated by Django 4.1.3 on 2022-11-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_alter_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(unique=True),
        ),
    ]
