# Generated by Django 5.0.4 on 2024-05-20 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billApp", "0007_delete_invoiceproductdetails"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvoiceProductDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("product_name", models.CharField(max_length=100)),
                ("product_description", models.TextField()),
                ("product_quantity", models.PositiveIntegerField()),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "bill_number",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billApp.billdetails",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billApp.userdetails",
                    ),
                ),
            ],
        ),
    ]