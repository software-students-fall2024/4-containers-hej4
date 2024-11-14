#FROM python:3.9
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#ADD . .
#EXPOSE 5000
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]
# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock first, then install dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --system

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
