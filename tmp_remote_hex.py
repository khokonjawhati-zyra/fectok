import paramiko

def check_file_hex():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- HEX DUMP of processed_pg_txs.json ---")
        # Find where it is. In docker it's in /app/auth_data/
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend xxd /app/auth_data/processed_pg_txs.json | head -n 2")
        print(stdout.read().decode())
        
        print("--- FILE LIST IN /app/auth_data/ ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend ls -la /app/auth_data/")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_file_hex()
