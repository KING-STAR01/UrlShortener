# Generated by Django 4.2.4 on 2023-08-09 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlDetail',
            fields=[
                ('long_url', models.CharField(db_index=True, max_length=512)),
                ('short_url', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
