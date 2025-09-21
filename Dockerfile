# Install latest Ubuntu Image
FROM ubuntu:latest

# Install Python3 and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean

# Create an activate a Python Virtual Environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements.txt over
COPY requirements.txt .

# Install Python3 Dependencies required for projects
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Verify dependencies have all been correctly installed, printed out during container initialization
RUN pip list > ./req_versions.txt

# Version of Flask
RUN flask --version

# Create dirs and set the working directory
WORKDIR /app
RUN mkdir -p /app/src

# Sleep forever, container never disappears
CMD ["bash", "-c", "while true; do sleep 3600; done"]

