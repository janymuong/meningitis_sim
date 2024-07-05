# meningitis_sim/seirs_sim/views.py

from django.shortcuts import render, redirect
from .parameters_form import (
    NormalSimulationForm,
    VaccineSimulationForm,
    AgeBasedVaccineSimulationForm
    )
from .meningitis import run_simulation
from .vaccination import vac_prob
from .vaccination_age import vac_prob_age


def normal_simulation(request):
    '''url/endpoint for a normal non-intervention sim
    '''
    if request.method == "POST":
        form = NormalSimulationForm(request.POST)
        if form.is_valid():
            parameters = form.save()
            run_simulation(parameters)
            return redirect('normal_simulation_result')
    else:
        form = NormalSimulationForm()
    return render(request, 'seirs_sim/parameters_form.html', {'form': form})

def normal_simulation_result(request):
    '''visualizations in terms of graphs for data-decision making'''
    return render(request, 'seirs_sim/normal_sim_result.html', 
                  {'image_path': 'static/figs/meningitis_dynamics.png'})

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


def age_based_vaccine_simulation(request):
    '''This route is for a simulation of a population with age-based vaccination'''
    if request.method == "POST":
        form = AgeBasedVaccineSimulationForm(request.POST)
        if form.is_valid():
            parameters = form.save(commit=False)
            probs = [float(prob.strip()) for prob in parameters.probs.split(',')]
            age_range = [float(age.strip()) for age in parameters.age_range.split(',')]
            vac_prob_age(probs=probs, age_range=age_range)
            return redirect('age_based_vaccine_simulation_result', probs=parameters.probs)
    else:
        form = AgeBasedVaccineSimulationForm()
    return render(request, 'seirs_sim/parameters_form.html', {'form': form})


def age_based_vaccine_simulation_result(request, probs):
    '''Visualization of the population dynamics after the age-based vaccination intervention'''
    probs_list = [float(prob.strip()) for prob in probs.split(',')]
    image_paths = [f'/figs/vaccine_9-18_moths{prob * 100}.png' for prob in probs_list]

    return render(request, 'seirs_sim/age_based_vaccine_sim_result.html', {'image_paths': image_paths})
