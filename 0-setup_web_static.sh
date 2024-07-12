#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment of web_static

# Install nginx if it's not already installed
sudo apt-get update
sudo apt install -y nginx

# Create data parent folder and subdirectories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html

# Create a fake HTML file with simple content
echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Creat a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Add location /hbnb_static/ block directive to /etc/nginx/sites-available/default
sudo sed -i '53i \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart
