#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static

# Install Nginx if not already installed
apt-get update
apt-get install -y nginx

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
cat > /data/web_static/releases/test/index.html << 'EOF'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create symbolic link (delete if exists, then recreate)
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve web_static content
nginx_config="/etc/nginx/sites-available/default"

# Check if the location block already exists
if ! grep -q "location /hbnb_static" "$nginx_config"; then
    # Add location block for hbnb_static before the first location block
    sed -i '/server_name _;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}' "$nginx_config"
fi

# Restart Nginx to apply changes
service nginx restart

exit 0
