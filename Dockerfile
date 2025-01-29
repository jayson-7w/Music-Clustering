# Use a base image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy app files into the container
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY model/ /app/model/

# Install uvicorn
RUN pip install uvicorn

EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]



# ## FLASK

# # Use a base image
# FROM python:3.10-slim-buster

# # Set working directory
# WORKDIR /app

# # Copy app files into the container
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY app.py .
# COPY model/ /app/model/

# EXPOSE 8080

# # Command to run the app
# CMD ["python", "app.py"]