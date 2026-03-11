import paramiko

def cleanup_v1_leftovers():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("FINALIZING CLEANUP OF LEGACY V1 BINARIES...")
        
        cmds = [
            "docker-compose --version",
            "rm -f /usr/bin/docker-compose || true",
            "ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/bin/docker-compose || true",
            "docker-compose version"
        ]
        
        for c in cmds:
            print(f"Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            print("STDOUT:", stdout.read().decode())
            print("STDERR:", stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_v1_leftovers()
