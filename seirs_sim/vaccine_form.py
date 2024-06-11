# meningitis_sim/seirs_sim/vaccine_form.py

from django import forms
from .models import SimulationParameters


class VaccineSimulationForm(forms.ModelForm):
    '''parameters for a simulation
    with vaccination as intervention'''
    class Meta:
        model = SimulationParameters
        fields = ['n_agents', 'n_timesteps', 'imm_boost']
        labels = {
            'n_agents': 'Population of Agents',
            'n_timesteps': 'Timesteps of Simulation',
            'imm_boost': 'Immunity Boost from Vaccination',
        }
