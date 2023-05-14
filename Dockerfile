FROM python:3.11

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt .

# Path: /app
RUN pip install -r requirements.txt

# Path: /app
COPY . .

EXPOSE 8000

# Path: /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```