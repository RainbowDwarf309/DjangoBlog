# Generated by Django 4.1.7 on 2023-04-15 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_favoritepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritepost',
            name='obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Post'),
        ),
    ]
