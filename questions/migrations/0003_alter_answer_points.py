# Generated by Django 4.2.7 on 2024-02-12 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0002_question_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="points",
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5),
        ),
    ]
