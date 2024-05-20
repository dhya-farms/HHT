FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
    
# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Run the application with Gunicorn

CMD ["gunicorn", "--config", "gunicorn.conf.py", "todo_project.wsgi:application"]