# Use a lightweight, secure base image
FROM python:3.11-slim

# Prevent Python from writing pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the functional workspace
WORKDIR /app

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application layers
COPY app.py .
COPY test_app.py .

# Expose network ingress port
EXPOSE 5000

# Run application using the standard entry point
CMD ["python", "app.py"]
