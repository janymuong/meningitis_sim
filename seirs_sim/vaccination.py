# meningitis_sim/seirs_sim/vaccination.py

import numpy as np
import sciris as sc
import starsim as ss
import matplotlib.pyplot as plt  # plotting/visualizations


class Vaccine(ss.Intervention):
    def __init__(self, timestep=100, prob=0.5, imm_boost=2.0):
        '''Initialize the intervention'''
        super().__init__()
        self.timestep = timestep # store the timestep the vaccine is applied on
        self.prob = prob # Store the probability of vaccination
        self.imm_boost = imm_boost # Store the amount by which immunity is boosted

    def apply(self, sim):
        ''' Apply the vaccine'''
        if sim.ti == self.timestep: # Only apply on the matching timestep
            meningitis = sim.diseases.meningitis
            eligible_ids = sim.people.uid[meningitis.susceptible]
            n_eligible = len(eligible_ids) # number of people who are eligible
            to_vaccinate = self.prob > np.random.rand(n_eligible) # define which of the n_eligible people get vaccinated
            vaccine_ids = eligible_ids[to_vaccinate]
            meningitis.immunity[vaccine_ids] += self.imm_boost

def vac_prob(probs=[0.3, 0.5]):
    from .simulator import make_sim

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
            vaccine_sim = make_sim(seed=seed, prob=prob, n_timesteps=n_timesteps, use_vaccine=True)
            baseline_sims.append(baseline_sim)
            vaccine_sims.append(vaccine_sim)

        def run_sim(sim):
            sim.run()
            results = sc.objdict()
            results.time = sim.yearvec
            results.n_infected = sim.results.meningitis.n_infected
            return results

        # run the simulations in parallel
        baseline_sim_results = sc.parallelize(run_sim, baseline_sims)
        vaccine_sim_results = sc.parallelize(run_sim, vaccine_sims)

        # pull out the results
        for seed in range(n_seeds):
            baseline = baseline_sim_results[seed]
            vaccine = vaccine_sim_results[seed]
            baseline_results[seed, :] = baseline.n_infected
            vaccine_results[seed, :] = vaccine.n_infected
            difference_results[seed] = baseline_results[seed, :].sum() - vaccine_results[seed, :].sum()

        # quantiles for plots;
        lower_bound_baseline = np.quantile(baseline_results, 0.05, axis=0)
        median_baseline = np.quantile(baseline_results, 0.5, axis=0)
        upper_bound_baseline = np.quantile(baseline_results, 0.95, axis=0)
        lower_bound_vaccine = np.quantile(vaccine_results, 0.05, axis=0)
        median_vaccine = np.quantile(vaccine_results, 0.5, axis=0)
        upper_bound_vaccine = np.quantile(vaccine_results, 0.95, axis=0)

        time = baseline.time # time vector for plotting

        # calculate differences
        lower_bound_diff = np.quantile(difference_results, 0.05)
        upper_bound_diff = np.quantile(difference_results, 0.95)
        median_diff = np.quantile(difference_results, 0.5)
        xx = prob * 100
        title = f'Estimated Impact: \n {median_diff:.0f} (90% CI: {lower_bound_diff:.0f}, {upper_bound_diff:.0f}) infections averted (Prob: {xx}%)'

        plt.figure()
        plt.title(title)
        plt.fill_between(time, lower_bound_baseline, upper_bound_baseline, alpha=0.5)
        plt.plot(time, median_baseline, label='Baseline')
        plt.fill_between(time, lower_bound_vaccine, upper_bound_vaccine, alpha=0.5)
        plt.plot(time, median_vaccine, label=f'With vaccine (Prob: {xx}%)')
        plt.xlabel('Time')
        plt.ylabel('Number of people infected')
        plt.legend()
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        image_filename = f'vaccine_whole_pop{xx}.png'
        image_path = f'static/figs/{image_filename}'
        plt.savefig(image_path)
        plt.close()  # close the plot to free up memory

    # timestep-based/the last generated image path
    return image_path  
