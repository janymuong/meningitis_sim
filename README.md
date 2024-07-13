# ![The Petri-Dish Posse](./static/img/thepetridish-posse-python.svg)
> ` ` Agent-Based Modeling: `Meningitis` ` ` 

This is a [**Python**](https://www.python.org/) implementation using the [`Starsim`](https://docs.idmod.org/projects/starsim/en/latest/) package.
We implement a `SIR`-like  model. Is extended to `SEIRs`:  

    - Susceptible
    - Exposed 
    - Infected
    - Recovered
    - etc  

Creating an intuitive `GUI` and the backend the server in [**Django**](https://www.djangoproject.com/), to set model parameters with minimum effort and view impactive visualizations for data-driven decisions, not gut feelings :) 


## Premise
Mathematical and computational models have become increasingly central in __epidemiological__ research, and particularly for __infectious diseases__. This solution is a system that bridges the gap between mathematical modelling and real-world problem domains to provide insights into how infection works in a population and gauge how intervention strategies (e.g. vaccination, treatment) can be used in the mix to counter infection. This would be used to make data-driven decisions or influence healthcare or lifestyle choices for individuals, agencies, organizations and even governments. In this context we use Agent-Based Modeling.

### WHAT `Agent-Based Modeling` IS
> Extending **SIR** to **SEIRs**  

Think of Agent-Based Modeling as a system of computational models that simulate behavior of individual agents in order to study emergent phenomena - in terms of disease infection in a population. Agents may represent *humans, institutions, microorganisms*, and *disease vectors* and so forth. The agents’ actions are based on autonomous decision-making and other behavioral traits, implemented through formal rules of interaction in an environment.  
Agent-based modeling provides a unique lens through which complex systems can be examined and understood. This allows for manipulating numerous variables to create detailed scenarios, offering insights into how different vaccination strategies, and treatment might perform under various epidemiological and social conditions.


> Read More on Agent-Based Modeling: [epidemix.jhubafrica.com](https://epidemix.jhubafrica.com/)  

<!-- <br/> -->

### Starsim
[Starsim](https://docs.idmod.org/projects/starsim/en/latest/) is an agent-based modeling framework in which users can design and configure simulations of diseases (or other health states) that progress over time within each agent and pass from one agent to the next along dynamic transmission networks. The framework explicitly supports co-transmission of multiple pathogens, allowing users to concurrently simulate several diseases while capturing behavioral and biological interactions. We use **Starsim** for the modeling and the simulating part of this project.


---
## Environment Set-Up

It's recommended to leverage a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [Python Docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).


- Create a siloed virtual environment with **Python 3.12** and **activate** it. You should have **Python 3.12** available in your host/local machine. 
Check the Python path using: 
```bash
$ which python3
```
```bash
$ python3 -m pip install --user virtualenv 
# on parent of root Django project directory;
# use a command similar to this one to create environment:
$ python3 -m virtualenv --python=<path-to-python3.12> ../.dj_sim
$ source ../.dj_sim/bin/activate
```
> Alternatively, you could setup the virtual environment via `make setup` in this [`Makefile`](./Makefile).

- Run `make install` to install **Django**, **Starsim** and other dependencies for it. This will install all relevant pip packages for the project.


```shell
$ cd meningitis_sim
$ code .
$
```


---
### Running Simulations
Each simulation runs in a Django environment:
```shell
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

(.dj_sim) mu-o@HP:~/django_sim/meningitis_sim$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

Starsim 0.3.4 (2024-04-18) — © 2023-2024 by IDM
System check identified no issues (0 silenced).
June 12, 2024 - 11:09:26
Django version 5.0.6, using settings 'meningitis_sim.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
