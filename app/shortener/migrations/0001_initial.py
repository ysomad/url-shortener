# Generated by Django 3.2 on 2021-07-17 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(max_length=2048, verbose_name='original URL')),
                ('code', models.CharField(blank=True, max_length=16, unique=True, verbose_name='unique code')),
                ('session', models.CharField(blank=True, max_length=256, null=True, verbose_name='session id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
            options={
                'db_table': 'shortened_urls',
            },
        ),
    ]
