# Generated by Django 5.0.6 on 2024-06-12 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sticky_notes_app", "0004_author_alter_poster_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="poster",
            name="temp_author",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
