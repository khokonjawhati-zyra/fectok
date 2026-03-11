import paramiko

def final_audit():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("INITIATING FINAL INFRA AUDIT...")
        
        cmds = [
            # 1. Port Conflict Audit
            "netstat -tulpn | grep ':80\|:443\|:5000' || echo 'PORTS_FREE'",
            
            # 2. Tooling Audit
            "which unzip || echo 'UNZIP_MISSING'",
            "python3 --version || echo 'PYTHON_MISSING'",
            
            # 3. Storage Audit
            "df -h / | tail -1",
            
            # 4. User/Permission Audit
            "groups root",
            
            # 5. Docker Storage Driver Audit
            "docker info | grep 'Storage Driver'",
            
            # 6. Final Docker Stress Test (Pull and Run)
            "docker run --rm hello-world"
        ]
        
        results = []
        for c in cmds:
            print(f"Audit: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            results.append(out if out else err)
            print(f"Result: {out if out else err}")
            
        ssh.close()
        
        # Validation Logic
        print("\n--- AUDIT SUMMARY ---")
        if "PORTS_FREE" in results[0]: print("[Sovereign Gateway] Ports 80/443/5000 are clear. ✅")
        else: print("[Sovereign Gateway] WARNING: Port conflict detected! ⚠️")
        
        if "unzip" in results[1]: print("[Deployment Tooling] Unzip is ready. ✅")
        if "Python 3" in results[2]: print("[Server Logic] Python 3 is ready. ✅")
        
        if "Hello from Docker!" in results[5]: print("[Docker Engine] Final execution test: PASSED. ✅")
        else: print("[Docker Engine] Final execution test: FAILED! ❌")
        
    except Exception as e:
        print(f"Error during final audit: {e}")

if __name__ == "__main__":
    final_audit()
