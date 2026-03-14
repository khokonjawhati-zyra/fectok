import paramiko
import os

def migrate_data():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    # 1. Ensure auth folder exists
    ssh.exec_command('mkdir -p /var/lib/sovereign/auth')
    
    # 2. Files to migrate
    files = [
        "media_vault.json",
        "ledger.json",
        "users_manifest.json",
        "sovereign_auth_vault.json",
        "config.json",
        "referral_map.json",
        "pending_tx.json",
        "processed_tx.json",
        "content_ownership.json",
        "trends_radar.json",
        "user_interest_matrix.json",
        "user_mood_matrix.json",
        "loyalty_ledger.json",
        "viral_pulse_ledger.json",
        "content_dna_ledger.json",
        "ai_fingerprint_ledger.json",
        "audio_insights_ledger.json"
    ]
    
    print("Migrating database files to persistent storage (/var/lib/sovereign/auth/)...")
    for f in files:
        # Use -n to not overwrite if exists, or -u to update. We probably want to overwrite with newest from backend if backend was just updated.
        # Actually, if backend was just updated via git/sftp, those files might be old.
        # But for now, let's just make sure they exist in the persistent volume.
        cmd = f'cp -v /root/sovereign/backend/{f} /var/lib/sovereign/auth/'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    # 3. Fix Permissions
    print("Fixing permissions...")
    ssh.exec_command('chmod -R 777 /var/lib/sovereign/auth/')
    
    # 4. Hard Cleanup
    print("Hard Resetting Ecosystem...")
    ssh.exec_command('cd /root/sovereign && docker-compose down && docker-compose up -d --build')
    # Use -v to clean up orphans if needed, but carefully
    
    ssh.close()
    print("MIGRATION & RESET COMPLETE.")

if __name__ == "__main__":
    migrate_data()
