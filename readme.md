# Country API

Geographical Information Service  
Python + FastAPI

## List of functionalities
- CRUD + authentication  
- Lists of countries visited by users  
- Lists of users favorite countries + ranking  
- Continent summaries

## Technology stack
- Python 3.12.7
- PostgreSQL 17.0
- Docker

## Units in Country
- inhabitants (residents) - million  
- area (total area of the country) - km²  
- GDP (gross domestic product) - billion USD

## Quick Start
- Navigate to the project directory  
- Build the application using Docker: `docker compose build`  
- Run the application using Docker: `docker compose up`  
- Use the Swagger UI at `http://localhost:8000/docs`  
- Create a new user using the `/register` endpoint  
- Log in using the `/token` endpoint  
- Use `Authorize` in Swagger by providing the appropriate `user_token` obtained from logging in  
- Try out the other endpoints

## Useful commands
- Install production dependencies: `pip install -r requirements.txt`  
- Install development dependencies: `pip install -r requirements-dev.txt`  
- Start the application server: `uvicorn countryapi.main:app --host 0.0.0.0 --port 8000`  
- API Documentation (Swagger): `http://localhost:8000/docs`  
- Build the project using Docker: `docker compose build` (to refresh the cache: `docker compose build --no-cache`)  
- Run the project using Docker: `docker compose up` (if the cache hasn't been refreshed: `docker compose up --force-recreate`)  
- Manually execute database queries (example queries in the init.sql file):  
  `-docker exec -it db psql -U postgres`  
  `\c app;`