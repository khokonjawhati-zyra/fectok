import os
import time
import sys
import subprocess
import json
import urllib.request
import tempfile
from dotenv import load_dotenv

# Force UTF-8 Output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# V15 Master Config: Resolve Dynamic Host Pulse
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), '.env')
load_dotenv(env_path)

# ═══════════════════════════════════════════════════════════════
# SOVEREIGN V15: MASTER DNA & ENVIRONMENT SENSING [PHASE 1]
# ═══════════════════════════════════════════════════════════════
IS_LINUX = os.name != 'nt'
IS_DOCKER = os.path.exists('/.dockerenv')

class EliteSovereignDNA:
    def __init__(self):
        # 1. OS-Aware Path Logic [DNA Healing]
        if IS_DOCKER:
            self.storage = "/app/vault/data"
        elif IS_LINUX:
            self.storage = "/var/www/html/media/videos" # Native R2 Mount Path
        else:
            self.storage = r"D:\server"
            
        self.ad_rotation = "1:6_RATIO"
        self.video_sharding = "5s_HLS_SEGMENTS"
        self.triple_slider = "ACTIVE"
        
        # Pillar Identity [AI_PROCESSOR]
        self.pillar = "AI_PROCESSOR"

# Initialize Sovereign Master Brain
SOV_DNA = EliteSovereignDNA()
# ═══════════════════════════════════════════════════════════════

def get_vault_path():
    # Sovereign V15: Standard Anchor Pulse from SOV_DNA
    base_vault = SOV_DNA.storage
    if not os.path.exists(base_vault):
        os.makedirs(base_vault, exist_ok=True)
    return base_vault

def find_ffmpeg():
    # Try system PATH first (Universal)
    try:
        # Check for both ffmpeg and ffmpeg.exe
        for cmd in ['ffmpeg', 'ffmpeg.exe']:
            if subprocess.run([cmd, '-version'], capture_output=True).returncode == 0:
                return cmd
    except:
        pass
    
    # Win32 Legacy Fallback (Local Development)
    if sys.platform == "win32":
        # Try WinGet path
        winget_base = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages')
        if os.path.exists(winget_base):
            for root, dirs, files in os.walk(winget_base):
                if 'ffmpeg.exe' in files:
                    return os.path.join(root, 'ffmpeg.exe')
    
    return 'ffmpeg' # Blind fallback for container environments where it's in PATH

def has_audio(file_path, ffmpeg_path):
    # Use ffprobe to check for audio streams
    ffprobe_path = ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe').replace('ffmpeg', 'ffprobe')
    try:
        result = subprocess.run([
            ffprobe_path, '-v', 'error', '-show_entries', 'stream=codec_type', 
            '-of', 'csv=p=0', file_path
        ], capture_output=True, text=True)
        return 'audio' in result.stdout
    except:
        return True # Fallback to true to try mixing anyway

def get_duration(file_path, ffmpeg_path):
    ffprobe_path = ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe').replace('ffmpeg', 'ffprobe')
    try:
        result = subprocess.run([
            ffprobe_path, '-v', 'error', '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', file_path
        ], capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return 0.0

# A_128: Setup Forensic Logging
LOG_FILE = os.path.join(get_vault_path(), "processor.log")
def log_event(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def process_video(file_path, vault_path):
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        log_event("ERROR: FFmpeg not found.")
        return

    log_event(f"[Sovereign Watcher] Processing Pulse Detected: {file_path}")
    
    # A_128: Wait for Neural Metadata (Max 10s)
    meta_path = file_path + ".json"
    wait_time = 0
    while not os.path.exists(meta_path) and wait_time < 10:
        time.sleep(1)
        wait_time += 1
    
    audio_mix_applied = False
    temp_merged_path = None
    input_file = file_path

    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            
            sound_url = meta.get("sound_url")
            orig_vol = meta.get("original_volume", 1.0)
            added_vol = meta.get("added_sound_volume", 0.5)

            if sound_url and sound_url.startswith("http"):
                log_event(f"[A_128] Neural Sync Triggered: {sound_url} found in meta.")
                # Download audio to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                    try:
                        urllib.request.urlretrieve(sound_url, tmp_audio.name)
                        audio_source = tmp_audio.name
                        log_event(f"[A_128] Audio Downloaded: {audio_source}")
                    except Exception as download_err:
                        log_event(f"[A_128 Error] Audio Download Failed: {download_err}")
                        audio_source = None

                if audio_source:
                    temp_merged_path = file_path.replace(".mp4", "_merged.mp4")
                    
                    # Sovereign Multi-Vault Resolver [A_128]
                    # We need to find the physical file on disk
                    filename = sound_url.split("/")[-1]
                    local_audio_path = None
                    
                    vault_paths = [vault_path, r"D:\server\sound_vault", os.path.join(os.getcwd(), "sound_vault")]
                    for vp in vault_paths:
                        potential_path = os.path.join(vp, filename)
                        if os.path.exists(potential_path):
                            local_audio_path = potential_path
                            break
                    
                    if local_audio_path:
                        audio_source = local_audio_path
                        log_event(f"[A_128] Neural Asset Resolved: {audio_source}")

                    if audio_source and os.path.exists(audio_source):
                        video_duration = get_duration(file_path, ffmpeg_path)
                        fade_start = max(0, video_duration - 2)
                        video_has_audio = has_audio(file_path, ffmpeg_path)
                        
                        # Sovereign V15: High-Context Mixing Strategy
                        # Case A: User wants only Added Sound (or Original silented)
                        if not video_has_audio or orig_vol <= 0.01:
                            log_event(f"[A_128] Strategy: REPLACEMENT [Target: {added_vol}]")
                            merge_cmd = [
                                ffmpeg_path, '-y',
                                '-i', file_path,
                                '-stream_loop', '-1', '-i', audio_source,
                                '-filter_complex', f'[1:a]volume={added_vol},afade=t=out:st={fade_start}:d=2[aout]',
                                '-map', '0:v', '-map', '[aout]',
                                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', '-ar', '44100',
                                '-shortest',
                                temp_merged_path
                            ]
                        # Case B: User wants only Original Sound (or Added silented)
                        elif added_vol <= 0.01:
                            log_event(f"[A_128] Strategy: ORIGINAL_ONLY [Target: {orig_vol}]")
                            merge_cmd = [
                                ffmpeg_path, '-y',
                                '-i', file_path,
                                '-filter_complex', f'[0:a]volume={orig_vol},afade=t=out:st={fade_start}:d=2[aout]',
                                '-map', '0:v', '-map', '[aout]',
                                '-c:v', 'copy', '-c:a', 'aac', '-ar', '44100',
                                temp_merged_path
                            ]
                        # Case C: Neural Amix Loop
                        else:
                            log_event(f"[A_128] Strategy: NEURAL_AMIX [Org: {orig_vol}, Add: {added_vol}]")
                            filter_complex = (
                                f'[0:a]volume={orig_vol}[a0];'
                                f'[1:a]volume={added_vol}[a1];'
                                f'[a0][a1]amix=inputs=2:duration=first:dropout_transition=2,'
                                f'afade=t=out:st={fade_start}:d=2[aout]'
                            )
                            merge_cmd = [
                                ffmpeg_path, '-y',
                                '-i', file_path,
                                '-stream_loop', '-1', '-i', audio_source,
                                '-filter_complex', filter_complex,
                                '-map', '0:v', '-map', '[aout]',
                                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', '-ar', '44100',
                                '-shortest',
                                temp_merged_path
                            ]
                        
                        mix_result = subprocess.run(merge_cmd, capture_output=True, text=True)
                        if mix_result.returncode == 0:
                            input_file = temp_merged_path
                            audio_mix_applied = True
                            log_event(f"[A_128] [SUCCESS] Neural Merge Locked: {temp_merged_path}")
                        else:
                            log_event(f"[A_128] [ERROR] FFmpeg Collision: {mix_result.stderr}")
                        
                        # Cleanup temp audio source ONLY if it was downloaded/extracted separately
                        # If it's a vault asset, LEAVE IT THERE for other users
                        if "vault" not in audio_source.lower():
                            if os.path.exists(audio_source):
                                os.remove(audio_source)
        except Exception as mix_err:
            log_event(f"[A_128] [CRITICAL] Neural Mixer Crash: {mix_err}")

    # Step 2: HLS Sharding & Sovereign Transformation (3:4 Map)
    file_name = os.path.basename(file_path).replace('.mp4', '')
    log_event(f"[A_125] Starting Universal Map Transformation (3:4) for {file_name}...")
    output_template = os.path.join(vault_path, f"{file_name}_%03d.ts")
    playlist_path = os.path.join(vault_path, f"{file_name}_master.m3u8")
    
    # Sovereign V15: The Universal Map Logic
    # 1. Scale to 1440 height (keeping aspect)
    # 2. Crop from center to 1080 width
    # 3. Final Output: 1080x1440 (3:4 Ratio)
    video_filter = (
        "scale='if(gt(a,3/4),-1,1080)':'if(gt(a,3/4),1440,-1)'," # Scale to fit 3:4 container
        "crop=1080:1440" # Force crop to 1080x1440 from center
    )

    cmd = [
        ffmpeg_path, '-y', '-i', input_file,
        '-vf', video_filter,
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k', 
        '-f', 'hls', '-hls_time', '5', '-hls_list_size', '0',
        '-hls_segment_filename', output_template,
        playlist_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        log_event(f"DONE: Video sharded at {playlist_path}")
        
        # Sovereign V15: Atomic Overwrite
        # Replace the original .mp4 with the audio-mixed version so raw playback works
        if temp_merged_path and os.path.exists(temp_merged_path):
            try:
                # Close any potential handles (though subprocess should be done)
                os.replace(temp_merged_path, file_path)
                log_event(f"[A_128] [SUCCESS] Original Video Replaced with Mixed Version.")
            except Exception as replace_err:
                log_event(f"[A_128 Error] Overwrite Failed: {replace_err}")
    except Exception as e:
        log_event(f"ERROR: Final processing failed: {e}")

if __name__ == "__main__":
    print("Sovereign Watcher Engine: ACTIVE [DNA_V15]")
    vault = get_vault_path()
    processed_files = set()

    # Disable pre-population to force scan of existing files
    # initial_files = [os.path.join(vault, f) for f in os.listdir(vault) if f.endswith('.mp4')]
    # processed_files.update(initial_files)

    while True:
        # Scan for .mp4 files in vault/data
        try:
            files = [f for f in os.listdir(vault) if f.endswith('.mp4')]
            for f in files:
                f_path = os.path.join(vault, f)
                if f_path not in processed_files:
                    # Sovereign V15: Atomic Upload Guard
                    # Check if file is still being written to (Race Condition Fix)
                    try:
                        size_initial = os.path.getsize(f_path)
                        time.sleep(2) # 2s Heart-beat check
                        size_final = os.path.getsize(f_path)
                        
                        if size_initial != size_final or size_final == 0:
                            print(f"[A_118] Upload in progress... skipping current pulse for {f}")
                            continue
                    except:
                        continue
                        
                    process_video(f_path, vault)
                    processed_files.add(f_path)
        except Exception as scan_err:
            print(f"Scan pulse error: {scan_err}")
            
        time.sleep(5) # Wait for next scan pulse (faster 5s)
