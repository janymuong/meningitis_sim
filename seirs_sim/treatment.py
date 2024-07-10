# meningitis_sim/seirs_sim/treatment.py

import numpy as np
import sciris as sc
import starsim as ss
import matplotlib.pyplot as plt


class Treatment(ss.Intervention):
    '''this class represents a generic treatment intervention'''

    def __init__(self, timestep=10, prob=0.5, mean_dur_infection=5):
        super().__init__() # initialize the intervention
        self.timestep = timestep # Store the timestep the treatment is applied on
        self.prob = prob # Store the probability of treatment
        self.dur_infection = ss.normal(mean_dur_infection, 1)  # store the duration of infection

    def apply(self, sim):
        if sim.ti == self.timestep: # Only apply on the matching timestep
            meningitis = sim.diseases.meningitis
            # Define  who is eligible for treatment
            eligible_ids = sim.people.uid[meningitis.ti_infected == sim.ti]  # People are eligible for treatment if they have just started exhibiting symptoms
            n_eligible = len(eligible_ids) # Number of people who are eligible
    
            # Define who receives treatment
            is_treated = np.random.rand(n_eligible) < self.prob  # Define which of the n_eligible people get treated by comparing np.random.rand() to self.p
            treat_ids = eligible_ids[is_treated]  # Pull out the IDs for the people receiving the treatment
    
            # Treated people will have a new disease progression
            dur_inf = self.dur_infection.rvs(treat_ids)  # Sample duration of infection by generating random variables (RVS) drawn from the distribution of durations
    
            # Determine who dies and who recovers and when
            will_die = meningitis.pars.p_death.rvs(treat_ids)  # Sample probability of dying
            dead_uids = treat_ids[will_die]  # Pull out the IDs of people who die
            recover_uids = treat_ids[~will_die]  # Pull out the IDs of people who recovery
            meningitis.ti_dead[dead_uids] = meningitis.ti_infected[dead_uids] + dur_inf[will_die] / sim.dt  # Set the time of death
            meningitis.ti_recovered[recover_uids] = meningitis.ti_infected[recover_uids] + dur_inf[~will_die] / sim.dt  # Set the time of recovery


def make_sim(seed=1, n_timesteps=100, use_treatment=False, timestep=20, prob=0.5, mean_dur_infection=5):
    '''make the simulation, but do not run it yet
    '''
    pars = dict(
        n_agents = 2000,
        start = 0,
        end = n_timesteps,
        dt = 1.0,
        verbose = 0,
        rand_seed = seed,
        networks = 'random',
        diseases = dict(
            type = 'meningitis',
        )
    )

    # Define "baseline" and "intervention" sims without and with the treatment
    if use_treatment:
        treatment = Treatment(timestep=timestep, prob=prob, mean_dur_infection=mean_dur_infection)
        sim = ss.Sim(pars, interventions=treatment)
    else:
        sim = ss.Sim(pars)

    return sim


def treat_prob(probs = [0.3, 0.5, 0.6, 0.8, 1]):
    for prob in probs:
        # Prepare to run multiple times
        n_seeds = 20  # Don't use too many here or your sim will take a very long time!
        n_timesteps = 100  # Again, don't use too many
        baseline_results = np.empty((n_seeds, n_timesteps+1))  # Initialize storage of baseline results
        treatment_results  = np.empty((n_seeds, n_timesteps+1))  # Initialize storage of treatment results
        difference_results = np.empty(n_seeds)  # Initialize storage of differences - this will tell us the impact
        baseline_sims = [] # Initialize the list of baseline simulations
        treatment_sims = [] # Initialize the list of baseline simulations
        
        # Make the simulations with different seeds
        for seed in range(n_seeds): # Run over 5 different random seeds
            baseline_sim = make_sim(seed=seed, n_timesteps=n_timesteps) # Run the simulation with no treatment
            treatment_sim  = make_sim(seed=seed, prob=prob, n_timesteps=n_timesteps, use_treatment=True) # Run the simulation with the treatment
            baseline_sims.append(baseline_sim) # Add the baseline sim to the list
            treatment_sims.append(treatment_sim) # Add the treatment sim to the list
        
        def run_sim(sim):
            """ Run the simulation and return the results """
            sim.run()
            results = sc.objdict()
            results.time = sim.yearvec
            results.n_infected = sim.results.meningitis.n_infected
            return results
        
        # Run the simulations in parallel
        baseline_sim_results = sc.parallelize(run_sim, baseline_sims) # Run baseline sims
        treatment_sim_results  = sc.parallelize(run_sim, treatment_sims) # Run the treatment sims
        
        
        # Pull out the results
        for seed in range(n_seeds):
            baseline = baseline_sim_results[seed]
            treatment = treatment_sim_results[seed]
            baseline_results[seed, :] = baseline.n_infected # Pull out results from baseline
            treatment_results[seed, :] = treatment.n_infected  # Pull out results from treatment scenarios
            difference_results[seed] = baseline_results[seed, :].sum() - treatment_results[seed, :].sum()  # Calculate differences
        
        # Get the qunatiles for plotting
        lower_bound_baseline = np.quantile(baseline_results, 0.05, axis=0)
        median_baseline      = np.quantile(baseline_results, 0.5, axis=0)
        upper_bound_baseline = np.quantile(baseline_results, 0.95, axis=0)
        lower_bound_treatment  = np.quantile(treatment_results, 0.05, axis=0)
        median_treatment       = np.quantile(treatment_results, 0.5, axis=0)
        upper_bound_treatment  = np.quantile(treatment_results, 0.95, axis=0)

        # Get the time vector for plotting
        time = baseline.time

        # Calculate differences
        lower_bound_diff = np.quantile(difference_results, 0.05)
        upper_bound_diff = np.quantile(difference_results, 0.95)
        median_diff = np.quantile(difference_results, 0.5)
        title = f'Estimated Impact: {median_diff:.0f} (90% CI: {lower_bound_diff:.0f}, {upper_bound_diff:.0f}) infections averted (Prob: {prob})'


        # visualizations/plots
        plt.figure()  # create the figure
        plt.title(title)
        plt.fill_between(time, lower_bound_baseline, upper_bound_baseline, alpha=0.5) # plot the uncertainty bound for baseline
        plt.plot(time, median_baseline, label='Baseline') # Plot the median for baseline
        plt.fill_between(time, lower_bound_treatment, upper_bound_treatment, alpha=0.5) # Plot the uncertainty bound for treatment
        plt.plot(time, median_treatment, label='With treatment') # Plot the median for treatment
        plt.xlabel('Time')
        plt.ylabel('Number of people infected')
        plt.legend() # Add legend
        plt.ylim(bottom=0) # Star the y-axis at 0
        plt.xlim(left=0) # Start the x-axis at 0
        image_filename = f'treatment_visualization{prob}.png'
        image_path = f'static/figs/{image_filename}'
        plt.savefig(image_path)
        # plt.show()
        plt.close() # cleanup - free up memory

    return image_path
