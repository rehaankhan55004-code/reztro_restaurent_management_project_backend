#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Microsoft ODBC Driver 17 for SQL Server on Render Linux
apt-get update && apt-get install -y curl gnupg
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Install Python dependencies
pip install -r requirements.txt