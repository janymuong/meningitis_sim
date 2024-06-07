.PHONY: setup-backend setup-frontend run-backend run-frontend

setup-backend:
	@echo "Setting up backend..."
	python -m virtualenv backend/venv
	source backend/venv/Scripts/activate  && pip install -r backend/requirements.txt

setup-frontend:
	@echo "Setting up frontend..."
	cd frontend && npm install

run-backend:
	@echo "Running backend..."
	cd backend && source venv/Scripts/activate && python app.py

run-frontend:
	@echo "Running frontend..."
	cd frontend && npm start

setup: setup-backend setup-frontend

run: run-backend run-frontend
