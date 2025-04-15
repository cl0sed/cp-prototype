FROM python:3.11-slim

# Install OS packages required for potential dependencies (like psycopg for Postgres)
# Using --no-install-recommends helps keep the image size down
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency definition files
COPY pyproject.toml poetry.lock* ./

# Compile production dependencies from pyproject.toml to requirements.txt
RUN uv pip compile pyproject.toml -o requirements.txt

# Install the compiled production dependencies using uv
# --system installs packages into the global site-packages
RUN uv pip install --system -r requirements.txt

# Copy the rest of the application code
# This comes after installing dependencies to leverage Docker cache
COPY . .

# Expose the API port
EXPOSE 8000

# Set default command to run the FastAPI API server via Uvicorn
# This can be overridden in docker-compose.yml for the worker service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
