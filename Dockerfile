# Use the alexmbarbosa/flask-python3 base image from Docker Hub
FROM alexmbarbosa/flask-python3

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install dependencies (if any)
# For example, if you have a requirements.txt file:
# RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your Flask app will run
EXPOSE 5000

# Define the command to run your Flask application
CMD ["python", "app.py"]

