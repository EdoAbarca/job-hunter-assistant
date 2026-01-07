FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper script
COPY scraper.py /app/

# Create output directory
RUN mkdir -p /app/output

# Create a non-root user
RUN useradd -m -u 1000 scraper && chown -R scraper:scraper /app
USER scraper

# Set the entrypoint
ENTRYPOINT ["python", "scraper.py"]
