import paramiko

def route_ui():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected to server. Ready to sync configuration.")
        
        nginx_conf = """
user  nginx;
worker_processes  auto;
events { worker_connections  1024; }
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile        on;

    server {
        listen 80;
        server_name fectok.com;
        root /usr/share/nginx/html/user;
        index index.html;

        add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";

        location / {
            try_files $uri $uri/ /index.html;
        }

        location ~ ^/(api/|ws/|login|register|forgot_password|reset_password|verify_registration|check_referral|verify_token) {
            proxy_pass http://backend_node:5000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /media/ {
            alias /usr/share/nginx/html/media/;
            autoindex on;
        }
    }

    server {
        listen 80;
        server_name vazo.fectok.com;
        root /usr/share/nginx/html/admin;
        index index.html;

        add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";

        location / {
            try_files $uri $uri/ /index.html;
        }

        location ~ ^/(api/|ws/|admin_auth_init|admin_auth_verify|verify_token|admin_config) {
            proxy_pass http://backend_node:5000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
"""
        full_compose = """version: '3.8'
services:
  backend_node:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: sovereign_v15_backend
    environment:
      - MODE=SCALABLE_PRODUCTION
      - SYSTEM_MODE=PRODUCTION
    volumes:
      - /var/lib/sovereign/auth:/app/auth_data
      - ./backend:/app
    ports:
      - "5000:5000"
    restart: always
    depends_on:
      - mirror_sync

  uplink_hub:
    build:
      context: ./sovereign_media_hub/uplink
      dockerfile: Dockerfile
    container_name: sovereign_v15_uplink
    volumes:
      - /var/www/html/media/videos:/app/vault/data
      - ./sovereign_media_hub/uplink:/app
    ports:
      - "8080:8080"
    restart: always

  mirror_sync:
    image: redis:latest
    container_name: sovereign_v15_redis
    ports:
      - "6379:6379"
    restart: always

  stream_gateway:
    image: nginx:alpine
    container_name: sovereign_v15_gateway
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./user_panel/build/web:/usr/share/nginx/html/user:ro
      - ./admin_panel/build/web:/usr/share/nginx/html/admin:ro
      - /var/www/html/media/videos:/usr/share/nginx/html/media:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - uplink_hub
      - backend_node
    restart: always

  ai_processor:
    build:
      context: ./sovereign_media_hub/processor
      dockerfile: Dockerfile
    container_name: sovereign_v15_processor
    volumes:
      - /var/www/html/media/videos:/app/vault/data
    restart: always

networks:
  default:
    name: sovereign_v15_mesh
"""

        sftp = ssh.open_sftp()
        with sftp.file("/root/sovereign/docker-compose.yml", "w") as f:
            f.write(full_compose)
        with sftp.file("/root/sovereign/nginx.conf", "w") as f:
            f.write(nginx_conf)
        sftp.close()
        
        ssh.close()
        print("Configuration files updated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    route_ui()
