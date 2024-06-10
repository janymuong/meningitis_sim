# meningitis_sim/seirs_sim/forms.py

from django import forms
from .models import SimulationParameters

class SimulationParametersForm(forms.ModelForm):
    class Meta:
        model = SimulationParameters
        fields = ['beta', 'init_prev', 'dur_inf']
        labels = {
            'beta': 'Infection Rate, ϐ',
            'init_prev': 'Initial prevalence',
            'dur_inf': 'Duration of infection',
        }
