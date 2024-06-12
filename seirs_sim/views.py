# meningitis_sim/seirs_sim/views.py

from django.shortcuts import render, redirect
from .normal_params_forms import SimulationParametersForm
from .vaccine_form import VaccineSimulationForm
from .simulation import run_simulation
from .vaccination import vac_prob

def normal_simulation(request):
    '''url/endpoint for a normal non-intervention sim
    '''
    if request.method == "POST":
        form = SimulationParametersForm(request.POST)
        if form.is_valid():
            parameters = form.save()
            run_simulation(parameters)
            return redirect('normal_simulation_result')
    else:
        form = SimulationParametersForm()
    return render(request, 'seirs_sim/parameters_form.html', {'form': form})

def normal_simulation_result(request):
    '''visualizations in terms of graphs for data-decision making'''
    return render(request, 'seirs_sim/normal_sim_result.html', {'image_path': 'static/figs/meningitis_dynamics.png'})

def vaccine_simulation(request):
    if request.method == "POST":
        form = VaccineSimulationForm(request.POST)
        if form.is_valid():
            parameters = form.save()
            run_simulation(parameters)
            vac_prob()
            return redirect('vaccine_simulation_result')
    else:
        form = VaccineSimulationForm()
    return render(request, 'seirs_sim/parameters_form.html', {'form': form})

def vaccine_simulation_result(request):
    img = ['static/figs/vaccine_whole_pop30.0.png', 'static/figs/vaccine_whole_pop50.0.png']
    return render(request, 'seirs_sim/vaccine_sim_result.html', {'image_path': img})

