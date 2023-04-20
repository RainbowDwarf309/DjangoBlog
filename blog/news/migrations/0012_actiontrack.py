# Generated by Django 4.1.7 on 2023-04-19 09:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0011_alter_userprofile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date of action')),
                ('ip', models.GenericIPAddressField(blank=None, null=True, unpack_ipv4=True, validators=[django.core.validators.validate_ipv46_address], verbose_name='Ip')),
                ('user_status', models.CharField(choices=[('Post publisher', 'Post Publisher'), ('Just user', 'Just User'), ('Staff', 'Staff'), ('Anonymous', 'Anonymous')], max_length=40, verbose_name='User status')),
                ('page', models.CharField(choices=[('Main(Index) page', 'Page Index'), ('Community page', 'Page Community'), ('Post profile(with comments) page', 'Post Profile'), ('Post submit page', 'Post Submit'), ('User profile page', 'User Profile'), ('User profile summary page', 'User Profile Summary'), ('User profile publications page', 'User Profile Publications'), ('User profile platform page', 'User Profile Platform'), ('Login page', 'Login'), ('Registration page', 'Registration'), ('Password reset view', 'Reset Password'), ('Password change view', 'Change Password'), ('Post API', 'Api Post'), ('Comment API utility', 'Api Comment Utility'), ('Post status -> DELETED', 'Post Deleted'), ('Favorite API', 'Api Favorite'), ('Karma', 'Karma')], max_length=100, verbose_name='Page')),
                ('page_url', models.URLField(max_length=500, verbose_name='Page URL')),
                ('action', models.CharField(choices=[('View', 'View'), ('Redirect', 'Go To'), ('Get object', 'Get Object'), ('Submit post', 'Submit Post'), ('View post', 'Post View'), ('Post utility plus 1', 'Post Utility Plus'), ('Post utility minus 1', 'Post Utility Minus'), ('Comment utility liked', 'Comment Utility Like'), ('Comment utility disliked', 'Comment Utility Dislike'), ('Create new child comment', 'Create New Child Comment')], max_length=100, verbose_name='Action')),
                ('action_reason', models.CharField(choices=[('Object not exist', 'Object Not Exist'), ("Haven't permissions", 'Havent Permissions'), ('Only owner can view (Object status) status', 'Object Status Only Owner'), ('Form invalid', 'Form Invalid'), ('Object submit spam', 'Object Submit Spam'), ('Coupon views change unsuccessfully. Already viewed', 'Post Already Viewed'), ('Coupon utility change unsuccessfully. Already changed', 'Post Utility Already Changed'), ('Comment utility change unsuccessfully. Already changed', 'Comment Utility Already Changed')], max_length=100, null=True, verbose_name='Reason')),
                ('details', models.TextField(blank=True, null=True, verbose_name='Details')),
                ('http_referer', models.TextField(null=True, verbose_name='Referer')),
                ('session_key', models.TextField(null=True, verbose_name='Session key')),
                ('user_agent', models.TextField(null=True, verbose_name='User agent')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='User', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
