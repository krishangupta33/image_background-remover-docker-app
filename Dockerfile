# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container to /app
WORKDIR /app

# Create the directory for the model
RUN mkdir -p /root/.u2net/

# download this https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
# This model is required by rembg for background removal
# COPY command copies the model file into the container's filesystem
COPY u2net.onnx /root/.u2net/u2net.onnx

# Verify model exists after copying
RUN ls -l /root/.u2net/u2net.onnx || echo "Model not found!"


# Copy the requirements.txt file from your local directory to the container
COPY requirements.txt .

# Install Python dependencies listed in requirements.txt
# --no-cache-dir reduces the image size by not caching pip packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining files from your local directory to the container
COPY . .

# Inform Docker that the container will listen on port 8501
EXPOSE 8501


# Streamlit specific configurations
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV HOME=/root

# Command to run when the container starts
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]