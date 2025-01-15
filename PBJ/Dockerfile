# Dockerfile für die Flask-Anwendung mit MariaDB

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies, einschließlich MariaDB-Client und MySQL-Client-Tools
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    default-libmysqlclient-dev \
    pkg-config \
    mariadb-client \
    && apt-get clean

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code and the SQL dump file
COPY . /app

# Kopiere die SQL-Datei in den Container (in ein temporäres Verzeichnis)
COPY user_system.sql /docker-entrypoint-initdb.d/

# Expose port 5000 (für die Flask-Anwendung)
EXPOSE 5000

# Start der MariaDB-Instanz, warte 10 Sekunden, führe SQL-Datei aus und starte Flask-Anwendung
CMD bash -c "service mysql start && sleep 10 && mysql -u root -pmy-secret-pw < /docker-entrypoint-initdb.d/user_system.sql && python app.py"
