FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your Python files
COPY . .

# Start the FastAPI server on port 7860 (Hugging Face default)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
