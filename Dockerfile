FROM python:3.12-slim

LABEL version="1.0.1" \
      description="Initial Experiment of Assesment App" \
      release.date="2025-09-14"

WORKDIR /cohere_assessment

# Install CA certificates and curl for debugging
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*


COPY ./requirements.txt /cohere_assessment/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /cohere_assessment/requirements.txt

COPY ./app /cohere_assessment/app

# Expose the port the app runs on
ENV APP_PORT=80
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port \${APP_PORT:-80}"