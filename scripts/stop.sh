#!/bin/bash
# Stop all services script

echo "🛑 Stopping ALGSOCH platform..."

docker-compose down

echo "✅ All services stopped!"
echo ""
echo "💡 To remove volumes: docker-compose down -v"
echo "💡 To remove images: docker-compose down --rmi all"
