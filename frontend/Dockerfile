# Stage 1: Build the SvelteKit application
FROM node:20-alpine as build

WORKDIR /app

# Copy package manifests
COPY package*.json ./

# Install build dependencies (using npm ci for consistency)
RUN npm ci

# Copy the rest of the frontend source code
COPY . .

# Build the application (output typically goes to /app/build with adapter-node)
RUN npm run build

# Stage 2: Run the Node.js server
FROM node:20-alpine

WORKDIR /app

# Install only production dependencies
# Copy package manifests from build stage
COPY --from=build /app/package*.json ./
# Install production modules
RUN npm ci --omit=dev

# Copy the built application output from the build stage
COPY --from=build /app/build ./build

# Expose the port the SvelteKit server listens on (default is 3000, can be overridden by PORT env var)
EXPOSE 3000

# Set the command to run the Node.js server
# Assumes adapter-node outputs 'index.js' as the entrypoint in the 'build' directory
CMD ["node", "build/index.js"]
