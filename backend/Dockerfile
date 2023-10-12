FROM python:3.11-slim

# Add a work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy app files
COPY . /app/

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]