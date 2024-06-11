# meningitis_sim/seirs_sim/normal_params_forms.py

from django import forms
from .models import SimulationParameters

class SimulationParametersForm(forms.ModelForm):
    '''parameters for a simulation
    no intervention'''
    class Meta:
        model = SimulationParameters
        fields = ['beta', 'init_prev', 'dur_inf']
        labels = {
            'beta': 'Infection Rate, ϐ',
            'init_prev': 'Initial prevalence',
            'dur_inf': 'Duration of infection',
        }

