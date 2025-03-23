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

# Expose the port Chainlit runs on
EXPOSE 8000

# Command to run the application
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]

# Add this line to your Dockerfile
RUN --mount=type=secret,id=openai_api_key \
    cat /run/secrets/openai_api_key > /app/.env

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY 