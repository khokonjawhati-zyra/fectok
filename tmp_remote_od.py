import paramiko

def check_file_od():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- OD DUMP of processed_pg_txs.json ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend od -t x1 /app/auth_data/processed_pg_txs.json")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_file_od()
