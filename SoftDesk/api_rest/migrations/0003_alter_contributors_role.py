# Generated by Django 4.2.1 on 2023-05-16 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0002_alter_issues_assignee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributors',
            name='role',
            field=models.CharField(choices=[('Auteur', 'Auteur'), ('Contributeur', 'Contributeur')], max_length=16),
        ),
    ]
