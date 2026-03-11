import paramiko

def fix_nginx():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("FIXING NGINX CONFIG...")
        
        # We use a raw string and write it via SFTP to avoid shell variable issues
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

        location ~ ^/(api/|ws/|login|register|forgot_password|reset_password|verify_registration|check_referral|verify_token|auth) {
            proxy_pass http://backend_node:5000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
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
        sftp = ssh.open_sftp()
        with sftp.file("/root/sovereign/nginx.conf", "w") as f:
            f.write(nginx_conf)
        sftp.close()
        
        print("RESTARTING GATEWAY...")
        ssh.exec_command("cd /root/sovereign && docker-compose restart stream_gateway")
        
        # Verify
        stdin, stdout, stderr = ssh.exec_command("docker ps")
        print(stdout.read().decode())
        
        ssh.close()
        print("--- NGINX FIXED ---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_nginx()
