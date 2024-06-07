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


age_data = pd.read_csv('nigeria_age.csv')

__all__ = ['Meningitis']

class Meningitis(SIR):
    def __init__(self, pars=None, par_dists=None, *args, **kwargs):
        """
        Initialize with parameters
        """
        pars = ss.omergeleft(pars,
            # add to default parameters;
            dur_exp_inf = 2,        # (days)
            dur_exp_rec = 2,        # (days)
            dur_inf = 14,        # (days)
            dur_rec = 7,        # (days)
            p_death = 0.05,    # (prob of death) 
            p_symptoms = 0.4,  # probability of showing symptoms 
            init_prev = 0.005, # Init cond
            beta = 0.08,         # Init cond
            rel_beta_inf = 0.5, # Reduction in transmission for I versus E
            waning = 1/(365*3),
            imm_boost = 0.001
        )
        
        par_dists = ss.omergeleft(par_dists,
            dur_exp_inf   = ss.normal,
            dur_exp_rec   = ss.normal,
            dur_inf   = ss.normal,
            dur_rec   = ss.normal,
            init_prev = ss.bernoulli,
            p_death   = ss.bernoulli,
            p_symptoms   = ss.bernoulli,
            imm_boost = ss.delta
        )

        super().__init__(pars=pars, par_dists=par_dists, *args, **kwargs)
        # SIR are added automatically, here we add E
        self.add_states(
            ss.State('exposed', bool, False),
            ss.State('ti_exposed', float, np.nan),
            #ss.State('ti_exposed_rec', float, np.nan),
            ss.State('ti_recovered', float, np.nan),
            ss.State('ti_susceptible', float, np.nan),
            # ss.State('ti_succeptible', float, np.nan),
            ss.State('immunity', float, 0.0),
        )
        return

    def init_results(self, sim):
        """ Initialize results """
        super().init_results(sim)
        self.results += ss.Result(self.name, 'rel_sus', sim.npts, dtype=float)
        self.results += ss.Result(self.name, 'new_recoveries', sim.npts, dtype=float)
        self.results += ss.Result(self.name, 'recovered', sim.npts, dtype=float)
        self.results += ss.Result(self.name, 'exposed', sim.npts, dtype=float)
        return

    def update_results(self, sim):
        """ Store the population immunity (susceptibility) """
        super().update_results(sim)
        self.results['rel_sus'][sim.ti] = self.rel_sus.mean()
        self.results['new_recoveries'][sim.ti] = np.count_nonzero(self.ti_recovered == sim.ti)
        self.results['recovered'][sim.ti] = np.count_nonzero(self.immunity > 1)
        self.results['exposed'][sim.ti] = self.exposed.sum()

        return 

    @property
    def infectious(self):
        return self.infected | self.exposed

    def update_pre(self, sim):
        # # Progress susceptible -> exposed
        # susceptible_exp = ss.true(self.susceptible & (self.ti_exposed <= sim.ti))
        # self.susceptible[susceptible_exp] = False
        # self.exposed[susceptible_exp] = True

        # Progress exposed -> recovered
        exposed_recovered = ss.true(self.exposed & (self.ti_recovered <= sim.ti))
        self.exposed[exposed_recovered] = False
        self.recovered[exposed_recovered] = True
        
        # Progress exposed -> infected
        infected = ss.true(self.exposed & (self.ti_infected <= sim.ti))
        self.exposed[infected] = False
        self.infected[infected] = True

        # Progress infected -> recovered
        recovered = ss.true(self.infected & (self.ti_recovered <= sim.ti))
        self.infected[recovered] = False
        self.recovered[recovered] = True

        # Progress recovered -> susceptible
        susceptible = ss.true(self.recovered & (self.ti_susceptible <= sim.ti))
        self.recovered[susceptible] = False
        self.susceptible[susceptible] = True
        self.update_immunity(sim)

        # Trigger deaths
        deaths = ss.true(self.ti_dead <= sim.ti)
        if len(deaths):
            sim.people.request_death(deaths)
        return

    def update_immunity(self, sim):
        uids = ss.true(self.immunity > 0)
        self.immunity[uids] = (self.immunity[uids])*(1 - self.pars.waning*sim.dt)
        self.rel_sus[uids] = np.maximum(0, 1 - self.immunity[uids])
        return

    def set_prognoses(self, sim, uids, source_uids=None):
        """ Set prognoses for those who get infected """
        # Do not call set_prognosis on parent
        # super().set_prognoses(sim, uids, source_uids)

        self.susceptible[uids] = False
        self.exposed[uids] = True
        self.ti_exposed[uids] = sim.ti

        p = self.pars
        self.immunity[uids] += p.imm_boost.rvs(uids)

        # Determine who will develop symptoms
        has_symptoms = p.p_symptoms.rvs(uids)
        symptomatic_uids = uids[has_symptoms]
        carrier_uids = uids[~has_symptoms]

        # Determine when exposed carriers recover
        self.ti_recovered[carrier_uids] = sim.ti + p.dur_exp_rec.rvs(carrier_uids) / sim.dt
        self.ti_susceptible[carrier_uids] = self.ti_recovered[carrier_uids] + p.dur_rec.rvs(carrier_uids) / sim.dt

        # Determine when exposed become infected for those who develop symptoms
        self.ti_infected[symptomatic_uids] = sim.ti + p.dur_exp_inf.rvs(symptomatic_uids) / sim.dt

        # Sample duration of infection, being careful to only sample from the
        # distribution once per timestep.
        dur_inf = p.dur_inf.rvs(symptomatic_uids)
        dur_rec = p.dur_rec.rvs(symptomatic_uids)
        
        # Determine when infected recover
        #self.ti_recovered[symptomatic_uids] = self.ti_infected[symptomatic_uids] + dur_inf / sim.dt # Check

        #dur_exp_rec = p.dur_rec.rvs(carrier_uids) # Check
        
        # Determine who dies and who recovers and when
        will_die = p.p_death.rvs(symptomatic_uids)
        dead_uids = symptomatic_uids[will_die]
        rec_uids = symptomatic_uids[~will_die]
        self.ti_dead[dead_uids] = self.ti_infected[dead_uids] + dur_inf[will_die] / sim.dt
        self.ti_recovered[rec_uids] = self.ti_infected[rec_uids] + dur_inf[~will_die] / sim.dt
        self.ti_susceptible[rec_uids] = self.ti_recovered[rec_uids] + dur_rec[~will_die] / sim.dt

        return

    def update_death(self, sim, uids):
        # Reset infected/recovered flags for dead agents
        for state in ['susceptible', 'exposed', 'infected', 'recovered']:
            self.statesdict[state][uids] = False
        return

    def make_new_cases(self, sim):
        """
        Add new cases of module, through transmission, incidence, etc.
        
        Common-random-number-safe transmission code works by mapping edges onto
        slots.
        """
        new_cases = []
        sources = []
        people = sim.people
        beta = self.pars.beta[0][0]

        net = sim.networks[0]
        contacts = net.contacts
        rel_trans = (self.infectious & people.alive) * self.rel_trans
        rel_trans[self.infected] *= self.pars.rel_beta_inf # Modify transmissibility of people with symptoms
        rel_sus = (self.susceptible & people.alive) * self.rel_sus
        p1p2b0 = [contacts.p1, contacts.p2]
        p2p1b1 = [contacts.p2, contacts.p1]
        for src, trg in [p1p2b0, p2p1b1]:

            # Calculate probability of a->b transmission.
            beta_per_dt = net.beta_per_dt(disease_beta=beta, dt=people.dt) # TODO: should this be sim.dt?
            p_transmit = rel_trans[src] * rel_sus[trg] * beta_per_dt

            # Generate a new random number based on the two other random numbers -- 3x faster than `rvs = np.remainder(rvs_s + rvs_t, 1)`
            rvs_s = self.rng_source.rvs(src)
            rvs_t = self.rng_target.rvs(trg)
            rvs = rvs_s + rvs_t
            inds = np.where(rvs>1.0)[0]
            rvs[inds] -= 1
            
            new_cases_bool = rvs < p_transmit
            new_cases.append(trg[new_cases_bool])
            sources.append(src[new_cases_bool])
                
        # Tidy up
        if len(new_cases) and len(sources):
            new_cases = np.concatenate(new_cases)
            sources = np.concatenate(sources)
        else:
            new_cases = np.empty(0, dtype=int)
            sources = np.empty(0, dtype=int)
            
        if len(new_cases):
            self._set_cases(sim, new_cases, sources)
            
        return new_cases, sources
        
    def plot(self):
        """ Default plot for SEIRS model """
        fig = pl.figure()
        for rkey in ['susceptible', 'exposed', 'infected', 'recovered']:
            pl.plot(self.results['n_'+rkey], label=rkey.title())
        pl.legend()
        pl.close()
        return fig
    

class Vaccine(ss.Intervention):
    def __init__(self, timestep=100, prob=0.5, imm_boost=2.0):
        super().__init__()  # Initialize the intervention
        self.timestep = timestep  # Store the timestep the vaccine is applied on
        self.prob = prob  # Store the probability of vaccination
        self.imm_boost = imm_boost  # Store the amount by which immunity is boosted

    def apply(self, sim):  # Apply the vaccine
        if sim.ti == self.timestep:  # Only apply on the matching timestep
            meningitis = sim.diseases.meningitis  # Shorten the name of the disease module
            eligible_ids = sim.people.uid[meningitis.susceptible]  # Only susceptible people are eligible
            n_eligible = len(eligible_ids)  # Number of people who are eligible
            to_vaccinate = self.prob > np.random.rand(n_eligible)  # Define which of the n_eligible people get vaccinated
            vaccine_ids = eligible_ids[to_vaccinate]
            meningitis.immunity[vaccine_ids] += self.imm_boost

# Define People class
class People(ss.People):
    def update_post(self, sim):
        self.age[self.alive] += 1 / 365
        return self.age

# Function to create the simulation
def make_sim(seed=1, n_timesteps=50, use_vaccine=False, timestep=10, prob=0.5, imm_boost=2.0):
    pars = dict(
        n_agents=2000,
        start=0,
        end=n_timesteps,
        dt=1.0,
        verbose=0,
        rand_seed=seed,
        networks='random',
        diseases=dict(
            type='meningitis',
            waning=0.009,
        )
    )

    people = People(n_agents=2000, age_data=age_data)

    if use_vaccine:
        vaccine = Vaccine(timestep=timestep, prob=prob, imm_boost=imm_boost)
        sim = ss.Sim(pars, people=people, interventions=vaccine)
    else:
        sim = ss.Sim(pars, people=people)

    return sim

# Function to run simulations with different vaccination probabilities
def vac_prob(probs=[0.3, 0.5]):
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

        baseline_sim_results = sc.parallelize(run_sim, baseline_sims)
        vaccine_sim_results = sc.parallelize(run_sim, vaccine_sims)

        for seed in range(n_seeds):
            baseline = baseline_sim_results[seed]
            vaccine = vaccine_sim_results[seed]
            baseline_results[seed, :] = baseline.n_infected
            vaccine_results[seed, :] = vaccine.n_infected
            difference_results[seed] = baseline_results[seed, :].sum() - vaccine_results[seed, :].sum()

        lower_bound_baseline = np.quantile(baseline_results, 0.05, axis=0)
        median_baseline = np.quantile(baseline_results, 0.5, axis=0)
        upper_bound_baseline = np.quantile(baseline_results, 0.95, axis=0)
        lower_bound_vaccine = np.quantile(vaccine_results, 0.05, axis=0)
        median_vaccine = np.quantile(vaccine_results, 0.5, axis=0)
        upper_bound_vaccine = np.quantile(vaccine_results, 0.95, axis=0)

        time = baseline_sim_results[0].time

        lower_bound_diff = np.quantile(difference_results, 0.05)
        upper_bound_diff = np.quantile(difference_results, 0.95)
        median_diff = np.quantile(difference_results, 0.5)
        xx = prob * 100
        title = f'Estimated impact: {median_diff:.0f} (90% CI: {lower_bound_diff:.0f}, {upper_bound_diff:.0f}) infections averted (Prob: {xx}%)'

        plt.figure()
        plt.title(title)
        plt.fill_between(time, lower_bound_baseline, upper_bound_baseline, alpha=0.5, label='Baseline 90% CI')
        plt.plot(time, median_baseline, label='Baseline Median')
        plt.fill_between(time, lower_bound_vaccine, upper_bound_vaccine, alpha=0.5, label='Vaccine 90% CI')
        plt.plot(time, median_vaccine, label='With Vaccine Median')
        plt.xlabel('Time')
        plt.ylabel('Number of people infected')
        plt.legend()
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        plt.savefig(f'figs/vaccine_whole_pop{xx}.png')
        plt.show()