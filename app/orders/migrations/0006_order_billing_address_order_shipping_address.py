# Generated by Django 4.2.10 on 2024-03-21 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0004_alter_address_options_rename_street_address_line1_and_more"),
        ("orders", "0005_order_invoice_file_order_razorpay_invoice_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="billing_address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="billing_orders",
                to="customers.address",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shipping_orders",
                to="customers.address",
            ),
        ),
    ]