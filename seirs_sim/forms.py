# meningitis_sim/seirs_sim/forms.py

from django import forms
from .models import SimulationParameters

class SimulationParametersForm(forms.ModelForm):
    class Meta:
        model = SimulationParameters
        fields = ['start', 'end', 'dt', 'prob', 'timestep', 'imm_boost', 'use_vaccine']
