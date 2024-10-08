# Generated by Django 5.0.2 on 2024-09-21 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer_management", "0005_lead_organisation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lead",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="customer_management.agent",
            ),
        ),
    ]
