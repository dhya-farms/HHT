# Generated by Django 4.2.10 on 2024-02-22 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="returnitem",
            old_name="return_order",
            new_name="return_obj",
        ),
    ]
