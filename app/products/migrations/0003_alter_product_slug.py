# Generated by Django 4.2.10 on 2024-03-13 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_category_icon_alter_category_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
