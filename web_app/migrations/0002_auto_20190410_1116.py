# Generated by Django 2.2 on 2019-04-10 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='ip',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='recaptcha',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]
