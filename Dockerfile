# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /backend

# Copy the current directory contents into the container at /app
COPY . /backend

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Django
ENV DJANGO_SETTINGS_MODULE=p2pPlatform.settings

# Expose the port that the Django app will run on
EXPOSE 8080

# Start the Django development server
#CMD ["echo", "====CREATING DB [START]===="]
#CMD ["python", "create_db.py"]
#CMD ["echo", "====CREATING DB [END]===="]
#
#CMD ["echo", "====CREATING MIGRATIONS [START]===="]
#CMD ["python", "manage.py", "makemigrations"]
#CMD ["echo", "====CREATING MIGRATIONS [END]===="]
#
#
#CMD ["echo", "====MIGRATING [START]===="]
#CMD ["python", "manage.py", "migrate"]
#CMD ["echo", "====MIGRATING [END]===="]
#
#CMD ["echo", "====RUNNING [START]===="]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
CMD ["bash", "build.sh"]