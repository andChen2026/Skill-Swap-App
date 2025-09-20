# Set the Image name
IMAGE_NAME = "app"

# Run 'docker build' for different hardwares
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t your-image-name:latest \
  --push .  # or --load if you want it locally

# Run 'docker run' in VSCode as an integrated terminal, remove once done
docker run -it -p --rm 8080:80 app

