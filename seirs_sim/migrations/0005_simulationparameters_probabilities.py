# Generated by Django 5.0.6 on 2024-06-13 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seirs_sim', '0004_simulationparameters_n_agents_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulationparameters',
            name='probabilities',
            field=models.TextField(default='0.3, 0.5', help_text='Enter proportion of population vaccinated separared by commas eg 0.3, 0.5'),
        ),
    ]
