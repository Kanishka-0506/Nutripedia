FROM python:3.12-slim

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p uploads && chmod 777 uploads

# Copy app files
COPY . .

# Start your app (update this if your file is named differently)
CMD ["python", "app.py"]
