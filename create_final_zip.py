import zipfile
import os

def create_mirror_zip():
    zip_name = "sovereign_v1.5.3_final_mirror.zip"
    script_dir = os.getcwd()
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Backend
        for root, dirs, files in os.walk("backend"):
            for file in files:
                zipf.write(os.path.join(root, file))
        
        # 2. Media Hub
        for root, dirs, files in os.walk("sovereign_media_hub"):
            for file in files:
                zipf.write(os.path.join(root, file))
                
        # 3. Web Admin Panel (Built)
        admin_build_path = os.path.join("admin_panel", "build", "web")
        for root, dirs, files in os.walk(admin_build_path):
            for file in files:
                filepath = os.path.join(root, file)
                # Map to webadmin_panel in zip
                arcname = os.path.join("webadmin_panel", os.path.relpath(filepath, admin_build_path))
                zipf.write(filepath, arcname)
                
        # 4. Web User Panel (Built)
        user_build_path = os.path.join("user_panel", "build", "web")
        for root, dirs, files in os.walk(user_build_path):
            for file in files:
                filepath = os.path.join(root, file)
                # Map to webuser_panel in zip
                arcname = os.path.join("webuser_panel", os.path.relpath(filepath, user_build_path))
                zipf.write(filepath, arcname)
                
        # 5. Root files
        zipf.write("docker-compose.yml")
        zipf.write("nginx.conf")
        
    print(f"MIRROR ZIP CREATED: {zip_name}")

if __name__ == "__main__":
    create_mirror_zip()
