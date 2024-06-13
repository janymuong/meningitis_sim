## The Petri-Dish Posse  
> Agent-Based Modeling: `Meningitis`  

This is an implementation of an`Agent-Based Model` using `Starsim` Python package.
We implement a `SIR`-like  model. Is extended to `SEIRs`:  

    - Susceptible
    - Exposed 
    - Infected
    - Recovered
    - etc
  

Creating the `GUI` and the backend the server in **Django**, to set model parameters with minimum effort and view visualization. 

---
## Background Context
Mathematical and computational models have become increasingly central in __epidemiological__ research, and particularly for __infectious diseases__. This solution is a system that bridges the gap between mathematical modelling and real-world problem domains to provide insights into how infection works in a population and gauge how intervention strategies (e.g. vaccination, treatment) can be used in the mix to counter infection. This would be used to make data-driven decisions or influence healthcare or lifestyle choices for individuals, agencies, organizations and even governments. In this context we use Agent-Based Modeling.

### WHAT `Agent-Based Modelling` IS
> Extending **SIR** to **SEIRs**


Think of Agent-Based Modeling as a system of computational models that simulate behavior of individual agents in order to study emergent phenomena - in terms of disease infection in a population. Agents may represent *humans, institutions, microorganisms*, and *disease vectors* and so forth. The agents’ actions are based on autonomous decision-making and other behavioral traits, implemented through formal rules of interaction in an environment.  
Agent-based modeling provides a unique lens through which complex systems can be examined and understood. This allows for manipulating numerous variables to create detailed scenarios, offering insights into how different vaccination strategies, and treatment might perform under various epidemiological and social conditions.


> ### Read More:
> [epidemix.jhubafrica.com/](https://epidemix.jhubafrica.com/)  


---
## `Environment Set-Up`

It's recommended to leverage a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [Python Docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).


- Create a siloed virtual environment with **Python 3.12** and **activate** it. You should have **Python 3.12** available in your host/local machine. 
Check the Python path using 
```bash
which python3
```
```bash
python3 -m pip install --user virtualenv 
# on parent of root Django project directory;
# use a command similar to this one to create environment:
python3 -m virtualenv --python=<path-to-python3.12> ../.dj_sim
source ../.dj_sim/bin/activate
```
> Alternatively, you could setup the virtualenv via `make setup` this [`Makefile`](./Makefile) is from a directive in.

- Run `make install` to install Django, Starsim and other necessary dependencies. This will install all relevant pip packages for the project.

### Running the Simulation
```shell
# python manage.py makemigrations
# python manage.py migrate

python manage.py runserver
```

```bash
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


---
```shell
$ cd meningitis_sim
$ code .
$
```