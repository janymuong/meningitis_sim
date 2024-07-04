# meningitis_sim/seirs_sim/parameters_form.py

from django import forms
from .models import SimulationParameters

class NormalSimulationParametersForm(forms.ModelForm):
    '''parameters for a simulation
    no intervention'''
    class Meta:
        model = SimulationParameters
        fields = ['beta', 'init_prev', 'dur_inf']
        labels = {
            'beta': 'Infection Rate, ϐ:',
            'init_prev': 'Initial prevalence:',
            'dur_inf': 'Duration of infection (days):',
        }
        widgets = {
            'beta': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0', 'max': '1', 'step': '0.01',
                'class': 'slider',
                'id': 'beta-slider'
            }),
            'init_prev': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0', 'max': '1', 'step': '0.001',
                'class': 'slider',
                'id': 'init-prev-slider'
            }),
            'dur_inf': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0', 'max': '100', 'step': '1',
                'class': 'slider',
                'id': 'dur-inf-slider'
            }),
        }


class VaccineSimulationForm(forms.ModelForm):
    '''parameters for a simulation
    with vaccination as intervention'''
    class Meta:
        model = SimulationParameters
        fields = ['n_agents', 'n_timesteps', 'probs', 'imm_boost']
        labels = {
            'n_agents': 'Population of Agents:',
            'n_timesteps': 'Timesteps of Simulation:',
            'probs': 'Proportions of Vaccinated People (comma-separated):',
            'imm_boost': 'Immunity Boost from Vaccination:'
        }
        widgets = {
            'n_agents': forms.NumberInput(attrs={
                'type': 'range',
                'min': '100', 'max': '10000', 'step': '100',
                'class': 'slider',
                'id': 'n-agents-slider'
            }),
            'n_timesteps': forms.NumberInput(attrs={
                'type': 'range',
                'min': '10', 'max': '60', 'step': '10',
                'class': 'slider',
                'id': 'n-timesteps-slider'
            }),
            'imm_boost': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0', 'max': '5', 'step': '0.1',
                'class': 'slider',
                'id': 'imm-boost-slider'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(VaccineSimulationForm, self).__init__(*args, **kwargs)
        self.fields['imm_boost'].initial = 2.0


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
            'n_agents': forms.NumberInput(attrs={
                'type': 'range',
                'min': '100', 'max': '10000', 'step': '100',
                'class': 'slider',
                'id': 'n-agents-slider'
            }),
            'n_timesteps': forms.NumberInput(attrs={
                'type': 'range',
                'min': '10', 'max': '1000', 'step': '10',
                'class': 'slider',
                'id': 'n-timesteps-slider'
            }),
            'imm_boost': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0', 'max': '5', 'step': '0.1',
                'class': 'slider',
                'id': 'imm-boost-slider'
            }),
            'probs': forms.TextInput(attrs={'placeholder': 'Comma-separated probabilities, e.g "0.5,1.0"'}),
            'age_range': forms.TextInput(attrs={'placeholder': 'Age range in years, e.g., "0.75,1.5"'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AgeBasedVaccineSimulationForm, self).__init__(*args, **kwargs)
        self.fields['imm_boost'].initial = 2.0
        self.fields['probs'].initial = '0.5,1.0'
