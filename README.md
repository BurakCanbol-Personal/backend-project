# Backend Project

This project is a backend system for managing datasets and running processing pipelines.

## Features
- Dataset creation and retrieval
- Pipeline execution per dataset
- Role-based access control
- Structured logging
- Persistent storage with Docker

## Tech Stack
- Python (Flask)
- Docker
- JSON storage

## Endpoints
- GET /datasets
- GET /datasets/<id>
- POST /datasets
- POST /pipeline/run/<id>