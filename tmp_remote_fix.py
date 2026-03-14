import paramiko

def fix_remote_encoding():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- FIXING processed_pg_txs.json ---")
        # Overwrite with proper UTF-8 []
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend sh -c \"echo '[]' > /app/auth_data/processed_pg_txs.json\"")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("--- VERIFYING ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend od -t x1 /app/auth_data/processed_pg_txs.json")
        print(stdout.read().decode())
        
        print("--- RESTARTING BACKEND ---")
        stdin, stdout, stderr = ssh.exec_command("docker restart sovereign_v15_backend")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_remote_encoding()
