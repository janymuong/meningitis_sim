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
    '''this route is for a simulation
    of a population that is vaccinated
    '''
    if request.method == "POST":
        form = VaccineSimulationForm(request.POST)
        if form.is_valid():
            parameters = form.save(commit=False)
            probs = [float(prob.strip()) for prob in parameters.probs.split(',')]
            run_simulation(parameters)
            vac_prob(probs=probs)  # pass probabilities to vac_prob function
            return redirect('vaccine_simulation_result', probs=parameters.probs)
    else:
        form = VaccineSimulationForm()
    return render(request, 'seirs_sim/parameters_form.html', {'form': form})

def vaccine_simulation_result(request, probs):
    '''visualization of the population dynamics after the intervention
    '''
    probs_list = [float(prob.strip()) for prob in probs.split(',')]
    image_paths = [f'/figs/vaccine_whole_pop{prob * 100}.png' for prob in probs_list]

    return render(request, 'seirs_sim/vaccine_sim_result.html', {'image_paths': image_paths})

