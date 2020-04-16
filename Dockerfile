# Develop stage
FROM node:11.1-alpine as develop-stage
#FROM node:13.13.0-alpine3.10 as develop-stage
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
# build stage
FROM develop-stage as build-stage
RUN yarn build

# Copy static docs to alpine-based nginx container.
FROM nginx:alpine

# Add bash
RUN apk add --no-cache bash

# Copy nginx configuration
COPY docker/default.conf /etc/nginx/conf.d/default.conf
COPY docker/nginx.conf /etc/nginx/nginx.conf

#COPY dist /usr/share/nginx/html
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Add non-privileged user
RUN adduser -D -u 1001 appuser

# Set ownership nginx.pid and cache folder in order to run nginx as non-root user
RUN touch /var/run/nginx.pid && \
    chown -R appuser /var/run/nginx.pid && \
    chown -R appuser /var/cache/nginx && \
    chown -R appuser /usr/share/nginx/html/

USER appuser

# Start Nginx server
CMD ["/bin/bash", "-c", "nginx -g \"daemon off;\""]
