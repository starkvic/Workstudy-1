# Generated by Django 4.2.2 on 2023-06-27 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cutomuser', '0004_alter_application_archived_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
