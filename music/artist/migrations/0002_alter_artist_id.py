# Generated by Django 4.1.7 on 2023-03-19 16:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=40, primary_key=True, serialize=False),
        ),
    ]
