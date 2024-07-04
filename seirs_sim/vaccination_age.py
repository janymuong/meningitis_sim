# meningitis_sim/seirs_sim/vaccination_age.py

import numpy as np
import sciris as sc
import starsim as ss
import pylab as pl  # plotting

class VaccineAge(ss.Intervention):
    def __init__(self, age_range=None, timestep=10, prob=0.5, imm_boost=2.0):
        super().__init__() # Initialize the intervention
        self.timestep = timestep # Store the timestep the vaccine is applied on
        self.prob = prob # Store the probability of vaccination
        self.imm_boost = imm_boost # Store the amount by which immunity is boosted
        self.age_range = age_range

    def apply(self, sim): # Apply the vaccine
        if sim.ti == self.timestep: # Only apply on the matching timestep
            meningitis = sim.diseases.meningitis # Shorten the name of the disease module
            eligibility_conditions = meningitis.susceptible
            
            if self.age_range is not None: 
                lower_age = self.age_range[0]
                upper_age = self.age_range[1]
                age_conditions = (sim.people.age >= lower_age) & (sim.people.age < upper_age)
                eligibility_conditions = eligibility_conditions & age_conditions
                
            eligible_ids = sim.people.uid[eligibility_conditions] # Only susceptible people are eligible
                
            n_eligible = len(eligible_ids)  # Number of people who are eligible
            to_vaccinate = self.prob > np.random.rand(n_eligible) # Define which of the n_eligible people get vaccinated
            vaccine_ids = eligible_ids[to_vaccinate]
            meningitis.immunity[vaccine_ids] += self.imm_boost

def vac_prob_age(probs=[0.5, 1.0], age_range=[0.75, 1.5]):
    from .simulator_age import make_sim

    for prob in probs:
        n_seeds = 20
        n_timesteps = 100
        baseline_results = np.empty((n_seeds, n_timesteps + 1))
        vaccine_results = np.empty((n_seeds, n_timesteps + 1))
        difference_results = np.empty(n_seeds)
        baseline_sims = []
        vaccine_sims = []

        for seed in range(n_seeds):
            baseline_sim = make_sim(seed=seed, n_timesteps=n_timesteps)
            vaccine_sim = make_sim(seed=seed, age_range=age_range, prob=prob, n_timesteps=n_timesteps, use_vaccine=True)
            baseline_sims.append(baseline_sim)
            vaccine_sims.append(vaccine_sim)

        def run_sim(sim):
            '''Run the simulation and return the results
            '''
            sim.run()
            results = sc.objdict()
            results.time = sim.yearvec
            results.n_infected = sim.results.meningitis.n_infected
            return results

        baseline_sim_results = sc.parallelize(run_sim, baseline_sims)
        vaccine_sim_results = sc.parallelize(run_sim, vaccine_sims)

        # pull out the results
        for seed in range(n_seeds):
            baseline = baseline_sim_results[seed]
            vaccine = vaccine_sim_results[seed]
            baseline_results[seed, :] = baseline.n_infected
            vaccine_results[seed, :] = vaccine.n_infected
            difference_results[seed] = baseline_results[seed, :].sum() - vaccine_results[seed, :].sum()

        # get the qunatiles for plotting
        lower_bound_baseline = np.quantile(baseline_results, 0.05, axis=0)
        median_baseline = np.quantile(baseline_results, 0.5, axis=0)
        upper_bound_baseline = np.quantile(baseline_results, 0.95, axis=0)
        lower_bound_vaccine = np.quantile(vaccine_results, 0.05, axis=0)
        median_vaccine = np.quantile(vaccine_results, 0.5, axis=0)
        upper_bound_vaccine = np.quantile(vaccine_results, 0.95, axis=0)

        # get the time vector for plotting
        time = baseline.time

        # calculate differences
        lower_bound_diff = np.quantile(difference_results, 0.05)
        upper_bound_diff = np.quantile(difference_results, 0.95)
        median_diff = np.quantile(difference_results, 0.5)
        xx = prob * 100
        title = f'Estimated Impact: \n {median_diff:.0f} (90% CI: {lower_bound_diff:.0f}, {upper_bound_diff:.0f}) infections averted (Prob: {xx}%)'

        pl.figure()
        pl.title(title)
        pl.fill_between(time, lower_bound_baseline, upper_bound_baseline, alpha=0.5)
        pl.plot(time, median_baseline, label='Baseline')
        pl.fill_between(time, lower_bound_vaccine, upper_bound_vaccine, alpha=0.5)
        pl.plot(time, median_vaccine, label=f'With vaccine (Prob: {xx}%)')
        pl.xlabel('Time')
        pl.ylabel('Number of people infected')
        pl.legend()
        pl.ylim(bottom=0)
        pl.xlim(left=0)
        image_filename = f'vaccine_9-18_moths{xx}.png'
        image_path = f'static/figs/{image_filename}'
        pl.savefig(image_path)
        pl.close()  # close the plot to free up memory

    return image_path
