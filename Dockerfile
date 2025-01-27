# Use a lightweight Python image
FROM python:3.9-slim

# Install system dependencies for OpenCV, PyTorch, YOLOv5, and Git
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Clone YOLOv5 repository
RUN git clone https://github.com/ultralytics/yolov5.git /yolov5

# Install Python dependencies for YOLOv5
RUN pip install --timeout=1000 --no-cache-dir -r /yolov5/requirements.txt


# Copy your project's requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application into the container
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
