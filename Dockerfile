# Use Python base image
FROM python:3.12-slim

# Update OS packages to include available security fixes
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Application port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
