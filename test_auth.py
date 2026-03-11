import paramiko

def test_auth():
    host = "167.71.193.34"
    user = "root"
    pw = "d!5.z6p*R&%*TM%"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Direct connection attempt to {host}...")
        ssh.connect(host, username=user, password=pw, look_for_keys=False, allow_agent=False)
        print("SUCCESS: Connected!")
        ssh.close()
    except paramiko.AuthenticationException:
        print("ERROR: Authentication failed (Wrong password or SSH config).")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_auth()
