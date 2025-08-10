#!/bin/bash

# Build and run Potato Disease Detection API with Docker

echo "🥔 Building Potato Disease Detection API Docker Image..."

# Build Docker image
docker build -t potato-disease-api .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    echo "🚀 Starting API container..."
    
    # Run container
    docker run -d \
        --name potato-disease-api \
        -p 8000:8000 \
        --restart unless-stopped \
        potato-disease-api
    
    if [ $? -eq 0 ]; then
        echo "✅ API container started successfully!"
        echo "🌐 API is running at: http://localhost:8000"
        echo "🔍 Health check: http://localhost:8000/health"
        echo "📋 API documentation: http://localhost:8000"
        echo ""
        echo "📊 Container status:"
        docker ps | grep potato-disease-api
        echo ""
        echo "📝 To view logs: docker logs potato-disease-api"
        echo "🛑 To stop: docker stop potato-disease-api"
        echo "🗑️ To remove: docker rm potato-disease-api"
    else
        echo "❌ Failed to start container"
        exit 1
    fi
else
    echo "❌ Failed to build Docker image"
    exit 1
fi
