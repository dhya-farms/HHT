# Generated by Django 4.2.10 on 2024-05-02 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_product_slug"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="role",
        ),
        migrations.AddField(
            model_name="user",
            name="favorites",
            field=models.ManyToManyField(blank=True, related_name="favorited_by", to="products.product"),
        ),
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.IntegerField(blank=True, choices=[(1, "Member"), (2, "President")], null=True),
        ),
    ]
