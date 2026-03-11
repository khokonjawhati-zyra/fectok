import paramiko

def sync_gateway_config():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("SYNCING DOCKER GATEWAY CONFIG...")
        
        # New Nginx Config for Dockerized Gateway
        # Backend is reachable as 'backend_node' within the docker network
        nginx_conf = """
user  nginx;
worker_processes  auto;
error_log  /var/log/nginx/error.log notice;
pid        /var/log/nginx.pid;
events { worker_connections  1024; }
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen 80;
        server_name fectok.com vazo.fectok.com localhost;

        location / {
            proxy_pass http://backend_node:5000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        location /media/ {
            alias /usr/share/nginx/html/media/;
            autoindex on;
        }
    }
}
"""
        
        cmds = [
            f"echo '{nginx_conf}' | tee /root/sovereign/nginx.conf > /dev/null",
            "cd /root/sovereign && docker-compose restart stream_gateway",
            "sleep 3",
            "docker logs sovereign_v15_gateway --tail 10"
        ]
        
        for c in cmds:
            print(f"\nExecuting: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # wait for exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            print(stdout.read().decode('utf-8', 'ignore'))
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_gateway_config()
