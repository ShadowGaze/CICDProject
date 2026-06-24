FROM python:3.13-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]