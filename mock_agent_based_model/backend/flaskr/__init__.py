from flask import Flask, request, jsonify
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
# origins=["http://localhost:3000"]
cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

# after_request decorator
@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,PUT'
    )
    return response


class Person(Agent):
    def __init__(self, unique_id, model, mobility_factor):
        super().__init__(unique_id, model)
        self.infected = False
        self.days_infected = 0
        self.mobility_factor = mobility_factor

    def move(self):
        x, y = self.pos
        neighborhood = self.model.grid.get_neighborhood((x, y), moore=True, include_center=False)
        cell_densities = [len(self.model.grid.get_cell_list_contents(pos)) for pos in neighborhood]
        weights = np.array([density ** self.mobility_factor for density in cell_densities])
        weights /= sum(weights)
        
        # find available cells by excluding non-empty cells
        empty_cells = [neighborhood[i] for i in range(len(neighborhood)) if self.model.grid.is_cell_empty(neighborhood[i])]
        
        if empty_cells:
            new_position = self.random.choices(empty_cells, weights=weights, k=1)[0]
            self.model.grid.move_agent(self, new_position)

    def infect(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        for neighbor in neighbors:
            if neighbor.infected and self.random.random() < 0.8:
                self.infected = True
                break

    def step(self):
        self.move()
        if not self.infected:
            self.infect()
        if self.infected:
            self.days_infected += 1

class DiseaseModel(Model):
    def __init__(self, N, width, height, mobility_factor):
        super().__init__()
        self.num_agents = N
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.mobility_factor = mobility_factor

        for i in range(self.num_agents):
            a = Person(i, self, mobility_factor=self.mobility_factor)
            self.schedule.add(a)
            placed = False
            while not placed:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if self.grid.is_cell_empty((x, y)):
                    self.grid.place_agent(a, (x, y))
                    placed = True

        agent = self.random.choice(self.schedule.agents)
        agent.infected = True

        self.datacollector = DataCollector(
            agent_reporters={"Infected": lambda a: a.infected,
                             "Days Infected": lambda a: a.days_infected})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    try:
        data = request.json
        num_agents = int(data['num_agents'])
        width = int(data['width'])
        height = int(data['height'])
        mobility_factor = float(data['mobility_factor'])

        model = DiseaseModel(num_agents, width, height, mobility_factor)
        for i in range(100):
            model.step()

        model_data = model.datacollector.get_agent_vars_dataframe()
        model_data.reset_index(inplace=True)

        return model_data.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
