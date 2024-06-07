from django.shortcuts import render, redirect
from .forms import SimulationParametersForm
from .models import SimulationParameters
import numpy as np
import sciris as sc
import starsim as ss
from starsim.diseases.sir import SIR
import pylab as pl # plotting
import matplotlib.pyplot as plt
import io
import urllib, base64
import matplotlib.pyplot as plt
import pandas as pd



# class Vaccine(ss.Intervention):
#     def __init__(self, timestep=100, prob=0.5, imm_boost=2.0):
#         super().__init__()  # Initialize the intervention
#         self.timestep = timestep  # Store the timestep the vaccine is applied on
#         self.prob = prob  # Store the probability of vaccination
#         self.imm_boost = imm_boost  # Store the amount by which immunity is boosted

#     def apply(self, sim):  # Apply the vaccine
#         if sim.ti == self.timestep:  # Only apply on the matching timestep
#             meningitis = sim.diseases.meningitis  # Shorten the name of the disease module
#             eligible_ids = sim.people.uid[meningitis.susceptible]  # Only susceptible people are eligible
#             n_eligible = len(eligible_ids)  # Number of people who are eligible
#             to_vaccinate = self.prob > np.random.rand(n_eligible)  # Define which of the n_eligible people get vaccinated
#             vaccine_ids = eligible_ids[to_vaccinate]
#             meningitis.immunity[vaccine_ids] += self.imm_boost

# # Define People class
# class People(ss.People):
#     def update_post(self, sim):
#         self.age[self.alive] += 1 / 365
#         return self.age

# # Function to create the simulation
# def make_sim(seed=1, n_timesteps=50, use_vaccine=False, timestep=10, prob=0.5, imm_boost=2.0):
#     pars = dict(
#         n_agents=2000,
#         start=0,
#         end=n_timesteps,
#         dt=1.0,
#         verbose=0,
#         rand_seed=seed,
#         networks='random',
#         diseases=dict(
#             type='meningitis',
#             waning=0.009,
#         )
#     )

#     people = People(n_agents=2000, age_data=age_data)

#     if use_vaccine:
#         vaccine = Vaccine(timestep=timestep, prob=prob, imm_boost=imm_boost)
#         sim = ss.Sim(pars, people=people, interventions=vaccine)
#     else:
#         sim = ss.Sim(pars, people=people)

#     return sim

# # Function to run simulations with different vaccination probabilities
# def vac_prob(probs=[0.3, 0.5]):
#     for prob in probs:
#         n_seeds = 20
#         n_timesteps = 100
#         baseline_results = np.empty((n_seeds, n_timesteps + 1))
#         vaccine_results = np.empty((n_seeds, n_timesteps + 1))
#         difference_results = np.empty(n_seeds)
#         baseline_sims = []
#         vaccine_sims = []

#         for seed in range(n_seeds):
#             baseline_sim = make_sim(seed=seed, n_timesteps=n_timesteps)
#             vaccine_sim = make_sim(seed=seed, prob=prob, n_timesteps=n_timesteps, use_vaccine=True)
#             baseline_sims.append(baseline_sim)
#             vaccine_sims.append(vaccine_sim)

#         def run_sim(sim):
#             sim.run()
#             results = sc.objdict()
#             results.time = sim.yearvec
#             results.n_infected = sim.results.meningitis.n_infected
#             return results

#         baseline_sim_results = sc.parallelize(run_sim, baseline_sims)
#         vaccine_sim_results = sc.parallelize(run_sim, vaccine_sims)

#         for seed in range(n_seeds):
#             baseline = baseline_sim_results[seed]
#             vaccine = vaccine_sim_results[seed]
#             baseline_results[seed, :] = baseline.n_infected
#             vaccine_results[seed, :] = vaccine.n_infected
#             difference_results[seed] = baseline_results[seed, :].sum() - vaccine_results[seed, :].sum()

#         lower_bound_baseline = np.quantile(baseline_results, 0.05, axis=0)
#         median_baseline = np.quantile(baseline_results, 0.5, axis=0)
#         upper_bound_baseline = np.quantile(baseline_results, 0.95, axis=0)
#         lower_bound_vaccine = np.quantile(vaccine_results, 0.05, axis=0)
#         median_vaccine = np.quantile(vaccine_results, 0.5, axis=0)
#         upper_bound_vaccine = np.quantile(vaccine_results, 0.95, axis=0)

#         time = baseline_sim_results[0].time

#         lower_bound_diff = np.quantile(difference_results, 0.05)
#         upper_bound_diff = np.quantile(difference_results, 0.95)
#         median_diff = np.quantile(difference_results, 0.5)
#         xx = prob * 100
#         title = f'Estimated impact: {median_diff:.0f} (90% CI: {lower_bound_diff:.0f}, {upper_bound_diff:.0f}) infections averted (Prob: {xx}%)'

#         plt.figure()
#         plt.title(title)
#         plt.fill_between(time, lower_bound_baseline, upper_bound_baseline, alpha=0.5, label='Baseline 90% CI')
#         plt.plot(time, median_baseline, label='Baseline Median')
#         plt.fill_between(time, lower_bound_vaccine, upper_bound_vaccine, alpha=0.5, label='Vaccine 90% CI')
#         plt.plot(time, median_vaccine, label='With Vaccine Median')
#         plt.xlabel('Time')
#         plt.ylabel('Number of people infected')
#         plt.legend()
#         plt.ylim(bottom=0)
#         plt.xlim(left=0)
#         plt.savefig(f'figs/vaccine_whole_pop{xx}.png')
#         plt.show()

# vac_prob()

def simulation_form(request):
    if request.method == 'POST':
        form = SimulationParametersForm(request.POST)
        if form.is_valid():
            params = form.save()
            return redirect('run_simulation', params.id)
    else:
        form = SimulationParametersForm()
    return render(request, 'seirs_sim/simulation_form.html', {'form': form})

# def run_simulation(request, params_id):
#     params = SimulationParameters.objects.get(id=params_id)
#     if params.use_vaccine is not None:
    
#         def make_sim(seed=1, n_timesteps=50, use_vaccine=False, timestep=10, prob=0.5, imm_boost=2.0):
#             pars = dict(
#                 n_agents=2000,
#                 start=params.start,
#                 end=params.end,
#                 dt=params.dt,
#                 verbose=0,
#                 rand_seed=seed,
#                 networks='random',
#                 diseases=dict(
#                     type='meningitis',
#                     waning=0.009,
#                 )
#             )
#             people = People(n_agents=2000, age_data=age_data)
#             if use_vaccine:
#                 vaccine = Vaccine(timestep=timestep, prob=prob, imm_boost=imm_boost)
#                 sim = ss.Sim(pars, people=people, interventions=vaccine)
#             else:
#                 sim = ss.Sim(pars, people=people)
#             return sim

#         n_seeds = 20
#         n_timesteps = params.end - params.start
#         baseline_results = np.empty((n_seeds, n_timesteps + 1))
#         vaccine_results = np.empty((n_seeds, n_timesteps + 1))
#         difference_results = np.empty(n_seeds)
#         baseline_sims = []
#         vaccine_sims = []

#         for seed in range(n_seeds):
#             baseline_sim = make_sim(seed=seed, n_timesteps=n_timesteps)
#             vaccine_sim = make_sim(seed=seed, prob=params.prob, n_timesteps=n_timesteps, use_vaccine=params.use_vaccine, timestep=params.timestep, imm_boost=params.imm_boost)
#             baseline_sims.append(baseline_sim)
#             vaccine_sims.append(vaccine_sim)

#         def run_sim(sim):
#             sim.run()
#             results = sc.objdict()
#             results.time = sim.yearvec
#             results.n_infected = sim.results.meningitis.n_infected
#             return results

#         baseline_sim_results = sc.parallelize(run_sim, baseline_sims)
#         vaccine_sim_results = sc.parallelize(run_sim, vaccine_sims)

#         for seed in range(n_seeds):
#             baseline = baseline_sim_results[seed]
#             vaccine = vaccine_sim_results[seed]
#             baseline_results[seed, :] = baseline.n_infected
#             vaccine_results[seed, :] = vaccine.n_infected
#             difference_results[seed] = baseline_results[seed, :].sum() - vaccine_results[seed, :].sum()

#         lower_bound_baseline = np.quantile(baseline_results, 0.05, axis=0)
#         median_baseline = np.quantile(baseline_results, 0.5, axis=0)
#         upper_bound_baseline = np.quantile(baseline_results, 0.95, axis=0)
#         lower_bound_vaccine = np.quantile(vaccine_results, 0.05, axis=0)
#         median_vaccine = np.quantile(vaccine_results, 0.5, axis=0)
#         upper_bound_vaccine = np.quantile(vaccine_results, 0.95, axis=0)
#         time = baseline_sim_results[0].time

#         lower_bound_diff = np.quantile(difference_results, 0.05)
#         upper_bound_diff = np.quantile(difference_results, 0.95)
#         median_diff = np.quantile(difference_results, 0.5)
#         xx = params.prob * 100
#         title = f'Estimated impact: {median_diff:.0f} (90% CI: {lower_bound_diff:.0f}, {upper_bound_diff:.0f}) infections averted (Prob: {xx}%)'

#         plt.figure()
#         plt.title(title)
#         plt.fill_between(time, lower_bound_baseline, upper_bound_baseline, alpha=0.5, label='Baseline 90% CI')
#         plt.plot(time, median_baseline, label='Baseline Median')
#         plt.fill_between(time, lower_bound_vaccine, upper_bound_vaccine, alpha=0.5, label='Vaccine 90% CI')
#         plt.plot(time, median_vaccine, label='With Vaccine Median')
#         plt.xlabel('Time')
#         plt.ylabel('Number of people infected')
#         plt.legend()
#         plt.ylim(bottom=0)
#         plt.xlim(left=0)
#         buffer = io.BytesIO()
#         plt.savefig(buffer, format='png')
#         buffer.seek(0)
#         image_png = buffer.getvalue()
#         buffer.close()
#         graphic = base64.b64encode(image_png)
#         graphic = graphic.decode('utf-8')

#         return render(request, 'seirs_sim/simulation_results.html', {'graphic': graphic})

#     else:
#         params = SimulationParameters.objects.get(id=params_id)
#         meningitis = Meningitis(beta=params.beta)
#         pars = dict(networks=dict(type='random'), start=params.start, end=params.end, dt=params.dt, verbose=0)
#         sim = ss.Sim(pars, diseases=meningitis)
#         sim.run()
#         fig = sim.diseases.meningitis.plot()

#         buf = io.BytesIO()
#         fig.savefig(buf, format='png')
#         buf.seek(0)
#         string = base64.b64encode(buf.read())
#         uri = 'data:image/png;base64,' + urllib.parse.quote(string)

#         return render(request, 'seirs_sim/simulation_result.html', {'image_uri': uri})

def run_simulation(request, params_id):
    params = SimulationParameters.objects.get(id=params_id)
    meningitis = Meningitis(beta=params.beta)
    pars = dict(networks=dict(type='random'), start=params.start, end=params.end, dt=params.dt, verbose=0)
    sim = ss.Sim(pars, diseases=meningitis)
    sim.run()
    fig = sim.diseases.meningitis.plot()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'seirs_sim/simulation_result.html', {'image_uri': uri})
