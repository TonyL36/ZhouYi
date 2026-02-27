# Stage 2: Serve with Nginx
FROM nginx:alpine

# Create directory structure for base path
RUN mkdir -p /usr/share/nginx/html/book/ZhouYi

# Copy build artifacts from build stage
COPY frontend/dist /usr/share/nginx/html/book/ZhouYi

# Copy Nginx configuration
COPY deployment/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]