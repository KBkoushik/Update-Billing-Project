# Generated by Django 5.0.4 on 2024-05-19 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billApp", "0002_alter_userdetails_user_company_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdetails",
            name="user_company_address",
            field=models.CharField(max_length=70),
        ),
    ]
