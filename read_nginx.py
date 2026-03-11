import paramiko

def read_nginx():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Project nginx.conf ---")
        stdin, stdout, stderr = ssh.exec_command("cat /root/sovereign/nginx.conf")
        print(stdout.read().decode('utf-8', 'ignore'))
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_nginx()
