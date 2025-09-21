# Shell script to build the image from the docker file
# Development only

# Set the Image name
IMAGE_NAME="itsandrewc/app"

# Log in to docker services
docker login

# Create and use a buildx builder that supports multi-platform
docker buildx rm multi-builder
docker buildx create --name multi-builder --use
docker buildx inspect --bootstrap

# Run 'docker build' for different hardwares
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $IMAGE_NAME:latest \
  --push \
  .  