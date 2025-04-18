FROM node:20-alpine AS base

# Setup base stage with dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Setup development stage (used for development with hot reload)
FROM base AS development
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
# We'll mount the src directory as a volume in docker-compose

# Setup build stage
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Setup production stage
FROM nginx:alpine AS production
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/dist .
COPY nginx.conf /etc/nginx/conf.d/default.conf

ENTRYPOINT ["nginx", "-g", "daemon off;"]
