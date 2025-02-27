# Portfolio Backend

This is the backend for the Portfolio application, built with FastAPI and SQLAlchemy.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- Python 3.7+
- pip (Python package manager)
- virtualenv

## Setting Up the Development Environment

1. Clone the repository:
   ```
   git clone https://github.com/tabnine-gtm/portfolio-backend.git
   cd portfolio-backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   ```
   cp .env.sample .env
   ```
   Open the `.env` file and replace the placeholder values with your actual configuration.

5. Initialize the database:
   ```
   rm -f portfolio.db
   alembic upgrade head
   ```

6. (Optional) Seed the database:
   ```
   python -m app.seed
   ```

## Running the Application

To run the application locally:

1. Ensure your virtual environment is activated.

2. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

3. The API will be available at `http://localhost:8000`.

## Database Migration

This project uses Alembic for database migrations. Here are some common commands:

- Create a new migration:
   ```
   alembic revision -m "Description of the changes"
   ```

- Apply all pending migrations:
   ```
   alembic upgrade head
   ```

- Revert the last migration:
   ```
   alembic downgrade -1
   ```

- View migration history:
   ```
   alembic history
   ```

For more detailed information on using Alembic, refer to the Alembic documentation.

## Project Structure

The project follows a modular structure to enhance maintainability and scalability:

portfolio-backend/
├── app/
│   ├── models/
│   │   └── ... (data models)
│   ├── routers/
│   │   └── ... (API routes)
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── .env
├── .env.sample
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── openapi.yaml
├── requirements.txt
└── setup.sh

- `app/`: Main application directory
  - `models/`: Contains data model definitions
  - `routers/`: Contains API route definitions
  - `auth.py`: Authentication-related functionality
  - `crud.py`: CRUD operations
  - `database.py`: Database connection and session management
  - `main.py`: Main FastAPI application entry point
  - `models.py`: SQLAlchemy models
  - `schemas.py`: Pydantic schemas for request/response validation
  - `seed.py`: Database seeding script
- `openapi.yaml`: OpenAPI specification
- `requirements.txt`: Python dependencies
- `setup.sh`: Setup script for the project

## API Documentation

Once the application is running, you can access the API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

You can also find the OpenAPI specification in the `openapi.yaml` file.

## Contributing

We welcome contributions to this project! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on how to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
