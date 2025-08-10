#!/bin/bash

# Deploy Potato Disease Detection API with Docker Compose

echo "🥔 Deploying Potato Disease Detection API..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose first."
    exit 1
fi

# Stop and remove existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🚀 Building and starting services..."
docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo "✅ API deployed successfully!"
    echo "🌐 API is running at: http://localhost:8000"
    echo "🔍 Health check: http://localhost:8000/health"
    echo "📋 API documentation: http://localhost:8000"
    echo ""
    echo "📊 Service status:"
    docker-compose ps
    echo ""
    echo "📝 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
    echo "🔄 To restart: docker-compose restart"
else
    echo "❌ Failed to deploy API"
    exit 1
fi
