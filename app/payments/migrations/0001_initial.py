# Generated by Django 4.2.10 on 2024-05-22 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("orders", "0001_initial"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_method",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Credit Card"),
                            (2, "Debit Card"),
                            (3, "Net Banking"),
                            (4, "UPI"),
                            (5, "Razorpay"),
                        ]
                    ),
                ),
                (
                    "payment_status",
                    models.PositiveSmallIntegerField(choices=[(1, "Pending"), (2, "Completed"), (3, "Failed")]),
                ),
                ("transaction_id", models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ("metadata", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="payments", to="orders.order"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Return",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.TextField()),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Requested"), (2, "Approved"), (3, "Rejected"), (4, "Returned")], default=1
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="returns", to="orders.order"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReturnItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product_variant",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="products.productvariant"),
                ),
                (
                    "return_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="return_items", to="payments.return"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Refund",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("refund_type", models.PositiveSmallIntegerField(choices=[(1, "Cancel"), (2, "Return")])),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("reason", models.TextField(blank=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Initiated"), (2, "Processed"), (3, "Completed"), (4, "Failed")]
                    ),
                ),
                ("metadata", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="refunds", to="payments.payment"
                    ),
                ),
                (
                    "return_obj",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="refund",
                        to="payments.return",
                    ),
                ),
            ],
        ),
    ]
