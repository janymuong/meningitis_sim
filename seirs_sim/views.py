# meningitis_sim/seirs_sim/views.py

from django.shortcuts import render, redirect
from .normal_params_forms import SimulationParametersForm
# from .models import SimulationParameters
from .simulation import run_simulation

def normal_simulation(request):
    if request.method == "POST":
        form = SimulationParametersForm(request.POST)
        if form.is_valid():
            parameters = form.save()
            run_simulation(parameters)
            return redirect('normal_simulation_result')
    else:
        form = SimulationParametersForm()
    return render(request, 'seirs_sim/normal_sim_form.html', {'form': form})

def normal_simulation_result(request):
    return render(request, 'seirs_sim/normal_sim_result.html', {'image_path': 'static/figs/meningitis_dynamics.png'})
