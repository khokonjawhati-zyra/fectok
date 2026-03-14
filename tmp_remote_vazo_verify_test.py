import paramiko

def check_verify_token_vazo():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- CURL https://vazo.fectok.com/verify_token ---")
        stdin, stdout, stderr = ssh.exec_command("curl -k -X POST -H 'Content-Type: application/json' -d '{\"token\":\"\"}' https://vazo.fectok.com/verify_token")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_verify_token_vazo()
