# Generated by Django 4.2.10 on 2024-03-13 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="icon",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/category_icons/"),
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/category_images/"),
        ),
        migrations.AlterField(
            model_name="category",
            name="placeholder",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/category_placeholders/"),
        ),
        migrations.AlterField(
            model_name="collection",
            name="icon",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/collection_icons/"),
        ),
        migrations.AlterField(
            model_name="collection",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/collection_images/"),
        ),
        migrations.AlterField(
            model_name="collection",
            name="placeholder",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/collection_placeholders/"),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/product_images/"),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="placeholder",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/product_placeholders/"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="icon",
            field=models.ImageField(blank=True, null=True, upload_to="merchandise/tag_icons/"),
        ),
    ]
