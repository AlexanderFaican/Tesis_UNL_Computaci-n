# Generated by Django 4.2.6 on 2023-12-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_car', '0004_medicioncompleto'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicioncompleto',
            name='collar_id',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
