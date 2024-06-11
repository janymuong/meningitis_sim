# meningitis_sim/seirs_sim/views.py

from django.shortcuts import render, redirect
from .forms import SimulationParametersForm
# from .models import SimulationParameters
from .simulation import run_simulation

def simulation_form(request):
    if request.method == "POST":
        form = SimulationParametersForm(request.POST)
        if form.is_valid():
            parameters = form.save()
            run_simulation(parameters)
            return redirect('simulation_result')
    else:
        form = SimulationParametersForm()
    return render(request, 'seirs_sim/simulation_form.html', {'form': form})

def simulation_result(request):
    return render(request, 'seirs_sim/simulation_result.html', {'image_path': 'static/figs/meningitis_dynamics.png'})
