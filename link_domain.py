import paramiko

def link_domain():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Linking fectok.com to backend...")
        
        # Nginx config template for both domains
        nginx_conf = """server {
    listen 80;
    server_name fectok.com vazo.fectok.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}"""
        
        cmds = [
            "apt-get update && apt-get install -y nginx",
            f"echo '{nginx_conf}' | tee /etc/nginx/sites-available/sovereign > /dev/null",
            "ln -sf /etc/nginx/sites-available/sovereign /etc/nginx/sites-enabled/",
            "rm -f /etc/nginx/sites-enabled/default",
            "nginx -t && systemctl restart nginx",
            "systemctl enable nginx"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            
        print("DOMAIN LINKED! Checking Port 80...")
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep :80")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    link_domain()
