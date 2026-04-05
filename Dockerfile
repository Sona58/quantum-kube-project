# Use a stable, slim Python 3.11 image for 2026 standards
FROM python:3.11-slim-bookworm

# 1. Security: Don't run as root (Vital for German/EU compliance)
RUN groupadd -r quantumuser && useradd -r -g quantumuser quantumuser

# 2. System dependencies (needed for some Qiskit transpiler optimizations)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Set up working directory
WORKDIR /app

# 4. Install Quantum & Production libraries
# We use 'qiskit' for the logic and 'fastapi' for the K8s interface
RUN pip install --no-cache-dir \
    qiskit==2.3.0 \
    qiskit-ibm-runtime==0.46.1 \
    fastapi \
    uvicorn

# 5. Switch to non-root user
USER quantumuser

# 6. Copy your code (we will create main.py next)
COPY --chown=quantumuser:quantumuser . .

# 7. Port for the K8s Service to hit
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]