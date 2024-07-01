# meningitis_sim/seirs_sim/simulator.py

import pandas as pd
# import numpy as np
# import sciris as sc
import starsim as ss

age_data = pd.read_csv('csv_data/nigeria_age.csv')


class People(ss.People):
    '''this is a class to define people
    meant to be a part the simulation
    '''
    def update_post(self, sim):
        self.age[self.alive] += 1/365
        return self.age
    
def make_sim(seed=1, n_agents=2000, n_timesteps=50, use_vaccine=False, timestep=10, prob=0.5, imm_boost=2.0):
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
        from .vaccination import Vaccine
        vaccine = Vaccine(timestep=timestep, prob=prob, imm_boost=imm_boost)
        sim = ss.Sim(pars, people=people, interventions=vaccine)
    else:
        sim = ss.Sim(pars, people=people)

    return sim
