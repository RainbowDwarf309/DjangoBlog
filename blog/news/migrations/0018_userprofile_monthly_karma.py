# Generated by Django 4.1.7 on 2023-05-08 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_favoritecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='monthly_karma',
            field=models.BigIntegerField(default=0, verbose_name='Monthly karma'),
        ),
    ]
