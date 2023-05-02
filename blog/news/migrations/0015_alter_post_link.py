# Generated by Django 4.1.7 on 2023-04-30 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_post_link_alter_post_author_alter_post_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.URLField(blank=True, default=None, null=True, unique=True, verbose_name='Instagram link'),
        ),
    ]
