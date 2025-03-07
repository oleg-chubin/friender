# Generated by Django 4.0.5 on 2022-07-06 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0005_friend_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='friend',
            name='hobbies',
            field=models.ManyToManyField(to='friends.hobby'),
        ),
    ]
