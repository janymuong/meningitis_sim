# meningitis_sim/seirs_sim/forms.py

from django import forms
from .models import SimulationParameters

class SimulationParametersForm(forms.ModelForm):
    class Meta:
        model = SimulationParameters
        fields = '__all__'
