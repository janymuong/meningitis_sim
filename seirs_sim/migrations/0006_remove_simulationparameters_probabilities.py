# Generated by Django 5.0.6 on 2024-06-13 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seirs_sim', '0005_simulationparameters_probabilities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulationparameters',
            name='probabilities',
        ),
    ]
