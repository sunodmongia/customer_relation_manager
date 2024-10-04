# Generated by Django 5.0.2 on 2024-09-29 18:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "customer_management",
            "0023_remove_agent_email_remove_agent_first_name_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="date_added",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="lead",
            name="email",
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="lead",
            name="phone_number",
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]