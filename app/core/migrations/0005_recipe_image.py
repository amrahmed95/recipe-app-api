# Generated by Django 3.2.25 on 2025-03-17 23:38

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20250317_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.recipe_image_file_path),
        ),
    ]
