# Generated by Django 3.2.11 on 2022-01-21 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_photoalbum_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
