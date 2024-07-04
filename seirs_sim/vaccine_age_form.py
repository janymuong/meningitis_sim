# meningitis_sim/seirs_sim/vaccine_age_form.py

from django import forms
from .models import SimulationParameters

class AgeBasedVaccineSimulationForm(forms.ModelForm):
    '''Parameters for a simulation with age-based vaccination as intervention'''
    class Meta:
        model = SimulationParameters
        fields = ['n_agents', 'n_timesteps', 'probs', 'imm_boost', 'age_range']
        labels = {
            'n_agents': 'Population of Agents:',
            'n_timesteps': 'Timesteps of Simulation:',
            'probs': 'Proportions of Vaccinated People (comma-separated) .e.g "0.5,1.0":',
            'imm_boost': 'Immunity Boost from Vaccination:',
            'age_range': 'Age Range for Vaccination (comma-separated lower and upper bounds, e.g., "0.75,1.5"):'
        }
        widgets = {
            'probs': forms.TextInput(attrs={'placeholder': 'Comma-separated probabilities, e.g "0.5,1.0"'}),
            'age_range': forms.TextInput(attrs={'placeholder': 'Age range in years, e.g., "0.75,1.5"'}),
        }
