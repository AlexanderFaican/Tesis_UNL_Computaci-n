# Generated by Django 5.0.2 on 2024-03-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_car', '0007_remove_medicioncompleto_humedad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicioncompleto',
            name='nombre_vaca',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
