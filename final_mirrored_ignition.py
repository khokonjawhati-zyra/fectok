import paramiko
import os
import time

def final_mirrored_ignition():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    local_zip = "sovereign_v1.5.3_mirror.zip"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=60)
        print("CONNECTED TO SERVER.")
        
        # 1. Transfer Local Zip
        print(f"UPLOADING {local_zip}...")
        sftp = ssh.open_sftp()
        sftp.put(local_zip, "/root/sovereign_v153.zip")
        sftp.close()
        print("TRANSFER SUCCESSFUL.")
        
        # 2. Extract and Configure
        print("EXTRACTING PROJECT...")
        # Clean current sovereign folder just in case
        ssh.exec_command("rm -rf /root/sovereign && mkdir -p /root/sovereign")
        stdin, stdout, stderr = ssh.exec_command("unzip -o /root/sovereign_v153.zip -d /root/sovereign/")
        stdout.channel.recv_exit_status()
        
        print("INJECTING CONFIGURATIONS...")
        nginx_conf = """
user  nginx;
worker_processes  auto;
events { worker_connections  1024; }
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile        on;

    # User Panel
    server {
        listen 80;
        server_name fectok.com;
        root /usr/share/nginx/html/user;
        index index.html;
        add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
        location / { try_files $uri $uri/ /index.html; }
        location ~ ^/(api/|ws/|login|register|forgot_password|reset_password|verify_token|check_referral) {
            proxy_pass http://backend_node:5000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        location /media/ { alias /usr/share/nginx/html/media/; autoindex on; }
    }

    # Admin Panel
    server {
        listen 80;
        server_name vazo.fectok.com;
        root /usr/share/nginx/html/admin;
        index index.html;
        add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
        location / { try_files $uri $uri/ /index.html; }
        location ~ ^/(api/|ws/|admin_auth_init|admin_auth_verify|verify_token|admin_config) {
            proxy_pass http://backend_node:5000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
        }
    }
}
"""
        docker_compose = """version: '3.8'
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
    ports: [ "5000:5000" ]
    restart: always
    depends_on: [ mirror_sync ]

  uplink_hub:
    build:
      context: ./sovereign_media_hub/uplink
      dockerfile: Dockerfile
    container_name: sovereign_v15_uplink
    volumes:
      - /var/www/html/media/videos:/app/vault/data
    ports: [ "8080:8080" ]
    restart: always

  mirror_sync:
    image: redis:latest
    container_name: sovereign_v15_redis
    ports: [ "6379:6379" ]
    restart: always

  stream_gateway:
    image: nginx:alpine
    container_name: sovereign_v15_gateway
    ports: [ "80:80", "443:443" ]
    volumes:
      - ./user_panel/build/web:/usr/share/nginx/html/user:ro
      - ./admin_panel/build/web:/usr/share/nginx/html/admin:ro
      - /var/www/html/media/videos:/usr/share/nginx/html/media:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on: [ mirror_sync, backend_node ]
    restart: always

  ai_processor:
    build:
      context: ./sovereign_media_hub/processor
    container_name: sovereign_v15_processor
    volumes: [ "/var/www/html/media/videos:/app/vault/data" ]
    restart: always

networks:
  default:
    name: sovereign_v15_mesh
"""
        sftp = ssh.open_sftp()
        with sftp.file("/root/sovereign/nginx.conf", "w") as f: f.write(nginx_conf)
        with sftp.file("/root/sovereign/docker-compose.yml", "w") as f: f.write(docker_compose)
        sftp.close()
        
        # 3. Activation
        print("DOCKER ACTIVATION...")
        cmds = [
            "cd /root/sovereign && docker-compose down || true",
            "cd /root/sovereign && docker-compose up -d --build",
            "docker ps"
        ]
        for c in cmds:
            print(f"Server Execute: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
        print("--- MISSION COMPLETE: V1.5.3 MIRROR IS LIVE ---")
        
    except Exception as e:
        print(f"CRITICAL SYNC ERROR: {e}")

if __name__ == "__main__":
    final_mirrored_ignition()
