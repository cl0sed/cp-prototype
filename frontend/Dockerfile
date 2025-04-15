# Dockerfile for the Frontend Application
#
# This file defines the steps to build the production Docker image for the SvelteKit frontend.
#
# Responsibilities typically involve:
# - Using a base Node.js image for building the app.
# - Copying package.json/lock files and installing dependencies.
# - Copying application source code.
# - Running the production build command (`npm run build`).
# - Using a multi-stage build to copy build artifacts (static assets)
#   into a lightweight server image (like Nginx or a minimal Node server).
# - Configuring the server (e.g., Nginx) to serve the static files correctly.
#
# Optimize for build speed (layer caching) and small final image size.
# Environment configuration (like API URLs) should typically be injected at runtime,
# not hardcoded in the image.
