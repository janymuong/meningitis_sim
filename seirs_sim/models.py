# meningitis_sim/seirs_sim/models.py

from django.db import models

class SimulationParameters(models.Model):
    # fields for a non-intervened infection dynamic
    beta = models.FloatField(default=0.1) # infection rate
    start = models.IntegerField(default=2000) # simulation start year
    end = models.IntegerField(default=2100) # end year 2,100
    dt = models.FloatField(default=1.0)
    
    # fields for vaccination
    use_vaccine = models.BooleanField(default=False)  # whether to use vaccine
    timestep = models.IntegerField(default=10)  # timestep to apply vaccine
    prob = models.FloatField(default=0.5)  # probability of vaccination
    imm_boost = models.FloatField(default=2.0)  # immunity boost from vaccine
