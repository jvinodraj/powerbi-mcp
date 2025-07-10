FROM python:3.11-slim

# Install .NET runtime for pythonnet/pyadomd
RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg wget ca-certificates && \
    wget -q https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends dotnet-runtime-8.0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure pythonnet to use the installed .NET runtime
ENV DOTNET_ROOT=/usr/lib/dotnet \
    PYTHONNET_RUNTIME=coreclr

WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "src/server.py"]
