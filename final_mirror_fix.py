import paramiko

def final_mirror_fix():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("RECONSTRUCTING SOVEREIGN V1.5.3 MIRROR...")
        
        cmds = [
            # 1. Kill everything
            "docker stop $(docker ps -aq) || true",
            "docker rm $(docker ps -aq) || true",
            
            # 2. Clean and Extract
            "rm -rf /root/sovereign",
            "mkdir -p /root/sovereign",
            "unzip -o /root/sovereign_v153.zip -d /root/sovereign_extract",
            
            # 3. Handle nesting (Some zips have a 'sovereign' folder inside)
            "if [ -d /root/sovereign_extract/sovereign ]; then mv /root/sovereign_extract/sovereign/* /root/sovereign/ && mv /root/sovereign_extract/sovereign/.* /root/sovereign/; else mv /root/sovereign_extract/* /root/sovereign/; fi",
            "rm -rf /root/sovereign_extract",
            
            # 4. Permissions
            "chmod -R 755 /root/sovereign",
            
            # 5. Verify paths
            "ls -F /root/sovereign/backend/main.py",
            "ls -F /root/sovereign/sovereign_media_hub/uplink/uplink_server.py",
            
            # 6. Inject Configs
            "cd /root/sovereign && python3 -c \"open('nginx.conf', 'w').write('''user  nginx;\\nworker_processes  auto;\\nevents { worker_connections  1024; }\\nhttp {\\n    include       /etc/nginx/mime.types;\\n    default_type  application/octet-stream;\\n    sendfile        on;\\n\\n    server {\\n        listen 80;\\n        server_name fectok.com;\\n        root /usr/share/nginx/html/user;\\n        index index.html;\\n        add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';\\n        location / { try_files $uri $uri/ /index.html; }\\n        location ~ ^/(api/|ws/|login|register|forgot_password|reset_password|verify_token|check_referral) {\\n            proxy_pass http://backend_node:5000;\\n            proxy_http_version 1.1;\\n            proxy_set_header Host $host;\\n            proxy_set_header X-Real-IP $remote_addr;\\n        }\\n        location /media/ { alias /usr/share/nginx/html/media/; autoindex on; }\\n    }\\n\\n    server {\\n        listen 80;\\n        server_name vazo.fectok.com;\\n        root /usr/share/nginx/html/admin;\\n        index index.html;\\n        add_header Cache-Control 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';\\n        location / { try_files $uri $uri/ /index.html; }\\n        location ~ ^/(api/|ws/|admin_auth_init|admin_auth_verify|verify_token|admin_config) {\\n            proxy_pass http://backend_node:5000;\\n            proxy_http_version 1.1;\\n            proxy_set_header Host $host;\\n        }\\n    }\\n}\\n''')\"",
            
            "cd /root/sovereign && python3 -c \"open('docker-compose.yml', 'w').write('''version: '3.8'\\nservices:\\n  backend_node:\\n    build: ./backend\\n    container_name: sovereign_v15_backend\\n    environment: [ MODE=SCALABLE_PRODUCTION, SYSTEM_MODE=PRODUCTION ]\\n    volumes: [ '/var/lib/sovereign/auth:/app/auth_data', './backend:/app' ]\\n    ports: [ '5000:5000' ]\\n    restart: always\\n\\n  uplink_hub:\\n    build: ./sovereign_media_hub/uplink\\n    container_name: sovereign_v15_uplink\\n    volumes: [ '/var/www/html/media/videos:/app/vault/data' ]\\n    ports: [ '8080:8080' ]\\n    restart: always\\n\\n  mirror_sync:\\n    image: redis:latest\\n    container_name: sovereign_v15_redis\\n    ports: [ '6379:6379' ]\\n    restart: always\\n\\n  stream_gateway:\\n    image: nginx:alpine\\n    container_name: sovereign_v15_gateway\\n    ports: [ '80:80', '443:443' ]\\n    volumes:\\n      - ./user_panel/build/web:/usr/share/nginx/html/user:ro\\n      - ./admin_panel/build/web:/usr/share/nginx/html/admin:ro\\n      - /var/www/html/media/videos:/usr/share/nginx/html/media:ro\\n      - ./nginx.conf:/etc/nginx/nginx.conf:ro\\n    depends_on: [ mirror_sync, backend_node ]\\n    restart: always\\n\\n  ai_processor:\\n    build: ./sovereign_media_hub/processor\\n    container_name: sovereign_v15_processor\\n    volumes: [ '/var/www/html/media/videos:/app/vault/data' ]\\n    restart: always\\n''')\"",
            
            # 7. Start
            "cd /root/sovereign && docker-compose up -d --build",
            
            "docker ps"
        ]
        
        for c in cmds:
            print(f"Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Use a longer timeout for unzip and compose
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
        print("--- MIRROR V1.5.3 FINAL RECONSTRUCTION COMPLETE ---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_mirror_fix()
