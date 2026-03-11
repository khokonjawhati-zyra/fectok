FROM python:3.12-slim-bookworm
WORKDIR /app

# Sovereign V15: Security Hardening Pulse
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    httpx \
    pydantic \
    python-dotenv \
    websockets \
    requests \
    google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib \
    PyJWT \
    passlib \
    pycryptodome \
    stripe

# Copy local code
COPY . .

# Sovereign V15: Expose Backend Pulse
EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
