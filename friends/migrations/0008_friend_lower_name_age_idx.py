# Generated by Django 4.0.5 on 2022-07-13 17:37

from django.db import migrations, models
import django.db.models.expressions
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0007_place_subjects'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='friend',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.functions.text.Lower('name')), django.db.models.expressions.F('age'), name='lower_name_age_idx'),
        ),
    ]
