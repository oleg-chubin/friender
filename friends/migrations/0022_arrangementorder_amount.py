# Generated by Django 4.0.5 on 2022-09-21 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0021_alter_establishmentrating_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrangementorder',
            name='amount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
