# Cloud requirements
Installation and Setup

## Clone the repository

git clone https://github.com/yourusername/yourrepository.git
cd yourrepository

## Set up a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

## Install dependencies:

pip install -r requirements.txt

## Set up Google Cloud authentication:

gcloud auth application-default login

## Configure the API Key for Gemini AI:
Replace "" in the genai.configure(api_key="") section of app.py with your Google AI API key.

## Run the application locally:

python app.py

The application should now be running at http://localhost:8080.

Deploying on Google Cloud

## Enable Cloud Run:

gcloud services enable run.googleapis.com

## Build and push Docker image:

gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/question-answering-app

Deploy to Cloud Run:

gcloud run deploy question-answering-app --image gcr.io/YOUR_PROJECT_ID/question-answering-app --platform managed --region YOUR_REGION --allow-unauthenticated

Replace YOUR_PROJECT_ID and YOUR_REGION with your Google Cloud project ID and desired deployment region.



## Docker Configuration

The application uses a Dockerfile for containerization:

# Use an official Python runtime as the base image
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip \
    && pip install gradio Flask google-generativeai scikit-learn

EXPOSE 8080
CMD ["python", "app.py"]

## Requirements

The requirements.txt file should include:
