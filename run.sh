# Set the Image name
IMAGE_NAME="app"

# Create a buildx object 

# Create and use a buildx builder that supports multi-platform
docker buildx create --name multi-builder --use
docker buildx inspect --bootstrap

# Run 'docker build' for different hardwares
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $IMAGE_NAME:latest \
  --push .  # or --load if you want it locally

# Run 'docker run' in VSCode as an integrated terminal, remove once done
docker run --rm -p 8080:5000 $IMAGE_NAME:latest

