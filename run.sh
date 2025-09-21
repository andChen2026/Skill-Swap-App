# Shell Script to run the image as a Container instance

# Set the Image name
IMAGE_NAME="itsandrewc/app"

# Find a dynamic port on the machine, exit if not
for port in {5000..5100}; do
  if ! lsof -iTCP:$port -sTCP:LISTEN >/dev/null; then
    FREE_PORT=$port
    break
  fi
done

# Run 'docker run' in VSCode as an integrated terminal, remove once done
docker run --rm -p $FREE_PORT:5000 $IMAGE_NAME:latest
