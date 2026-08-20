#!/bin/bash

# Day 4 - HiveMQ + InfluxDB + Grafana Setup Script

echo "=========================================="
echo "Day 4 - IoT System Setup"
echo "=========================================="

# Install Python dependencies
echo "Installing Python packages..."
pip install paho-mqtt influxdb-client gpiozero

# Create environment file
echo "Creating .env file..."
cat > .env << EOL
# HiveMQ Cloud Configuration
MQTT_HOST=xxxxxxxxx.s1.eu.hivemq.cloud
MQTT_PORT=8883
MQTT_USERNAME=your_hivemq_username
MQTT_PASSWORD=your_hivemq_password

# InfluxDB Cloud Configuration
INFLUX_URL=https://us-central1-1.gcp.cloud2.influxdata.com
INFLUX_TOKEN=your_influxdb_token
INFLUX_ORG=your_influxdb_org_id
INFLUX_BUCKET=your_influxdb_bucket_name
EOL

echo "Please edit .env with your actual credentials"

# Copy service file
echo "Copying systemd service file..."
sudo cp task9.service /etc/systemd/system/

# Reload systemd and enable service
sudo systemctl daemon-reload

echo "Setup complete!"
echo "=========================================="
echo "Next steps:"
echo "1. Edit .env file with your actual credentials"
echo "2. Run: python3 main.py"
echo "3. Or enable service: sudo systemctl enable task9.service"
echo "=========================================="
