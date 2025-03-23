# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements file
COPY requirements.txt .

# Install dependencies system-wide
RUN uv pip install --system -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for Hugging Face Spaces (required)
EXPOSE 7860

# Command to run the application on Hugging Face's required port
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"] 