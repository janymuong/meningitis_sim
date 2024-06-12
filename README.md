## Agent-Based Modeling: `Meningitis`

This is an implementation of an`Agent-Based Model` using `Starsim` Python package.
We implement a **SIR**-like  model. Is extended to `SEIRs`:  

    - Susceptible
    - Exposed 
    - Infected
    - Recovered
    - etc
  

Creating the `GUI` and the backend the server in Django, to set model parameters with minimum effort and view visualization. 

---
## Environment Set-Up

`Virtual Environments` - It's recommended to leverage a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).


- Create a siloed virtual environment with Python 3.7 and **activate** it. You should have Python 3.12 available in your host/local machine. 
Check the Python path using `which python3`
```bash
python3 -m pip install --user virtualenv 
# use a command similar to this one to create environment: on parent of Django app
python3 -m virtualenv --python=<path-to-python3.12> ../.dj_sim
source ../.dj_sim/bin/activate
```
> Alternatively, you could setup the virtualenv via `make setup`. [this](./Makefile) is from a directive in `Makefile`.

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