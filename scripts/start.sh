#!/bin/bash
# Start all services script

echo "🚀 Starting ALGSOCH platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building Docker images..."
docker-compose build

echo "🔄 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

echo "✅ Platform started successfully!"
echo ""
echo "📊 Access points:"
echo "  - Frontend:        http://localhost:5173"
echo "  - Python API:      http://localhost:8000"
echo "  - Java Analytics:  http://localhost:8080"
echo "  - API Docs:        http://localhost:8000/docs"
echo "  - Nginx Proxy:     http://localhost"
echo ""
echo "🔐 Default admin credentials:"
echo "  - Username: admin"
echo "  - Password: changeme"
echo ""
echo "📝 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
