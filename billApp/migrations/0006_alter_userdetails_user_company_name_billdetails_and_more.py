# Generated by Django 5.0.4 on 2024-05-20 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billApp", "0005_addproduct"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdetails",
            name="user_company_name",
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name="BillDetails",
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
                ("bill_number", models.CharField(max_length=6)),
                ("bill_date", models.DateField()),
                ("bill_time", models.TimeField()),
                ("customer_name", models.CharField(max_length=100)),
                ("customer_mobile_no", models.CharField(max_length=15)),
                ("customer_address", models.CharField(max_length=200)),
                ("bill_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billApp.userdetails",
                    ),
                ),
            ],
        ),
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
            ],
        ),
    ]
