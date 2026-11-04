# Module 11 – FastAPI Calculator with SQLAlchemy
Dockerhub:https://hub.docker.com/repository/docker/codeec/601_module11 
Github:https://github.com/DeepLearnDS/module11_is601

## Project Overview

This project extends the Module 10 FastAPI application by integrating SQLAlchemy database models and Pydantic schemas for calculation operations. It uses PostgreSQL for database storage and supports polymorphic inheritance for different calculation types.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Docker and Docker Compose
- Pytest
- GitHub Actions

## Calculation Model

The project implements a `Calculation` model using SQLAlchemy polymorphic inheritance.

The calculation types include:

- Addition
- Subtraction
- Multiplication
- Division

Each calculation stores:
- Calculation ID
- User ID
- Calculation type
- Inputs
- Result
- Creation timestamp
- Updated timestamp

The calculation model uses a shared database table and polymorphic identities to distinguish the different calculation types.

## Calculation Factory

The calculation factory creates the appropriate calculation subclass based on the requested calculation type.

It supports:
- Addition
- Subtraction
- Multiplication
- Division
- Multiple numeric inputs
- Input validation
- Division-by-zero validation

## Pydantic Schemas

The calculation schemas define and validate the data used by the application.

The schemas include:
- `CalculationType`
- `CalculationCreate`
- `CalculationUpdate`
- `CalculationResponse`
- `CalculationRead`

They validate calculation types, input lists, and required fields.

## Database

PostgreSQL is used as the database.

SQLAlchemy models define the database structure and relationships between users and calculations.

Docker Compose is used to configure the application and database services.

## Running the Application

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python main.py
```

The application runs at:

`http://127.0.0.1:8000`

Health endpoint:

`http://127.0.0.1:8000/health`

## Running with Docker

Build and start the containers:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

Stop containers:

```bash
docker compose down
```

## Running Tests

Run the complete test suite:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Test Results

The completed Module 11 test suite produced:

- 122 passed
- 1 skipped
- 0 failed
- 93% overall code coverage

## Project Objectives

The project demonstrates the integration of SQLAlchemy models, polymorphic inheritance, Pydantic validation, PostgreSQL database functionality, and automated testing within a FastAPI application.