# Generated by Django 4.2 on 2023-04-29 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='assignee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
