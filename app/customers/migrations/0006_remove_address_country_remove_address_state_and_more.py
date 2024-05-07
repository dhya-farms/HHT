# Generated by Django 4.2.10 on 2024-05-03 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0005_remove_address_customer_remove_review_customer_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="address",
            name="country",
        ),
        migrations.RemoveField(
            model_name="address",
            name="state",
        ),
        migrations.AlterField(
            model_name="address",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
