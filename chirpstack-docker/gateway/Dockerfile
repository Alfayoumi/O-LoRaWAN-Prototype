# Use a minimal Python image to run the gateway simulation
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    iproute2 \
    iperf3 \
    sudo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY gateway.py .

CMD ["python", "gateway.py"]
