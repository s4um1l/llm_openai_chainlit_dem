# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install uv as root
RUN pip install uv

# Copy requirements file
COPY requirements.txt .

# Install dependencies system-wide (as root)
RUN uv pip install --system -r requirements.txt

# Create a non-root user for running the application
RUN useradd -m -u 1000 user

# Create necessary directories for Chainlit and set permissions
RUN mkdir -p /app/.files /app/.cache && \
    chown -R user:user /app

# Copy the application code and set proper ownership
COPY --chown=user . .

# Switch to the non-root user for running the application
USER user

# Expose the port for Hugging Face Spaces (required)
EXPOSE 7860

# Command to run the application on Hugging Face's required port
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]