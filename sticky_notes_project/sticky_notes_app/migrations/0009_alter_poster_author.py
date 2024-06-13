# Generated by Django 5.0.6 on 2024-06-12 22:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sticky_notes_app", "0008_poster_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poster",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="sticky_notes_app.author",
            ),
        ),
    ]
