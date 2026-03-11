import paramiko

def check_server():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=10)
        print("SSH CONNECTION: OK")
        stdin, stdout, stderr = ssh.exec_command("ls -la /root/sovereign")
        print("STDOUT:", stdout.read().decode())
        print("STDERR:", stderr.read().decode())
        ssh.close()
    except Exception as e:
        print(f"SSH CONNECTION FAILED: {e}")

if __name__ == "__main__":
    check_server()
