# Generated by Django 5.2 on 2025-04-26 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_rename_budget_budget_amount_budget_year_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='month',
        ),
    ]
