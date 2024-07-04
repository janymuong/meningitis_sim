# meningitis_sim/seirs_sim/simulator_age.py

import pandas as pd
import starsim as ss

age_data = pd.read_csv('model_data/nigeria_age.csv')

class People(ss.People):
    def update_post(self, sim):
        self.age[self.alive] += 1/365
        return self.age

def make_sim(seed=1, n_agents=2000, n_timesteps=50, use_vaccine=False, timestep=10, prob=0.5, imm_boost=2.0, age_range=None):
    '''Make the simulation, but do not run it yet
    '''
    pars = dict(
        n_agents=n_agents,
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

    people = People(n_agents=n_agents, age_data=age_data)

    if use_vaccine:
        from .vaccination_age import VaccineAge
        vaccine = VaccineAge(timestep=timestep, age_range=age_range, prob=prob, imm_boost=imm_boost)
        sim = ss.Sim(pars, people=people, interventions=vaccine)
    else:
        sim = ss.Sim(pars, people=people)

    return sim
