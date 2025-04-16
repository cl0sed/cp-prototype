# ---- Builder Stage ----
FROM python:3.11 as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install uv

COPY pyproject.toml poetry.lock* ./

# Option 1: Compile inside build
RUN uv pip compile pyproject.toml -o requirements.txt
# Option 2: Copy pre-compiled (if done outside)
# COPY requirements.txt ./

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN uv pip install --no-cache-dir -r requirements.txt

# ---- Final Stage ----
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/venv ./venv

COPY . .

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
