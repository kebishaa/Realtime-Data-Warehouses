FROM apache/superset:latest

USER root

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir mysqlclient
RUN pip install pinotdb

# Set environment variables
ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

# Copy initialization script and configuration
COPY ./superset-init.sh /superset-init.sh
COPY superset_config.py /app/

# Set Superset config path
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

# Make the init script executable
RUN chmod +x /superset-init.sh

USER superset

# Set entrypoint
ENTRYPOINT ["/superset-init.sh"]
