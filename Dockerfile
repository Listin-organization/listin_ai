# 1. Start from a official, lightweight Python image
FROM python:3.11-slim

# 2. Set a "working directory" inside the container
WORKDIR /app

# 3. Copy ONLY the requirements file in first
# (Docker is smart and caches this layer)
COPY requirements.txt .

# 4. Install all your Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now, copy your *entire* project into the container
# This copies `main.py` and the `listin_agent` folder
COPY . .

# 6. Tell Google Cloud what port your app will be running on
ENV PORT 8080

# 7. The command to run when the container starts.
# This starts the FastAPI server.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]