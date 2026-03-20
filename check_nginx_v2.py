import paramiko

def check_nginx_v2():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        cmd = "find /etc/nginx -name '*.conf' | xargs grep -l 'fectok.com'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        files = stdout.read().decode().split()
        
        for f in files:
            print(f"--- {f} ---")
            stdin, stdout, stderr = ssh.exec_command(f"cat {f}")
            print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_nginx_v2()
