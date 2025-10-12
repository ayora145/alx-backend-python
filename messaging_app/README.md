# Messaging App - Docker Setup

## Prerequisites
- Docker installed
- Docker Compose installed

## Setup Instructions

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop services:**
   ```bash
   docker-compose down
   ```

5. **Stop services and remove volumes:**
   ```bash
   docker-compose down -v
   ```

## Environment Variables
Create a `.env` file with:
```
MYSQL_DB=messaging_app_db
MYSQL_USER=messaging_user
MYSQL_PASSWORD=messaging_password
MYSQL_ROOT_PASSWORD=root_password
```

## Services
- **web**: Django messaging app (port 8000)
- **db**: MySQL database (port 3306)

## Data Persistence
Database data is persisted using Docker volumes (`mysql_data`).