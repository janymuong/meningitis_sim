# meningitis_sim/seirs_sim/models.py

from django.db import models
# from django import forms

class SimulationParameters(models.Model):
    dur_exp_inf = models.FloatField(default=2.0)  # Duration exposed to infectious
    dur_exp_rec = models.FloatField(default=2.0)  # Duration exposed to recovered
    dur_inf = models.FloatField(default=14.0)     # Duration of infection
    dur_rec = models.FloatField(default=7.0)      # Duration of recovery
    p_death = models.FloatField(default=0.05)     # Probability of death
    p_symptoms = models.FloatField(default=0.4)   # Probability of showing symptoms
    init_prev = models.FloatField(default=0.005)  # Initial prevalence
    beta = models.FloatField(default=0.08)        # Transmission rate
    rel_beta_inf = models.FloatField(default=0.5) # Reduction in transmission for infected vs exposed
    waning = models.FloatField(default=1/1095)    # Immunity waning rate
    imm_boost = models.FloatField(default=0.001)  # Immunity boost

    # vaccine simulation model parameters;
    n_agents = models.IntegerField(default=2000)
    n_timesteps = models.IntegerField(default=20)
    # imm_boost = models.FloatField(default=0.001)

    def __str__(self):
        return f"Simulation Parameters {self.id}"
