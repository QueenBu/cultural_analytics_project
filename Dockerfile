FROM python:3.10-slim

# Install system dependencies for dlib & OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-python-dev \
    libboost-thread-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir face_recognition opencv-python-headless numpy

# Create working directory
WORKDIR /app

# Copy your script into the container
COPY . /app

CMD ["python", "main.py"]
