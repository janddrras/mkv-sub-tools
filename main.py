import os
import subprocess
import json
import sys
from pathlib import Path
import pysubs2

def get_mkv_info(mkv_path):
    """Returns the JSON info from mkvmerge."""
    try:
        result = subprocess.run(
            ["mkvmerge", "-J", str(mkv_path)],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting MKV info: {e.stderr}")
        return None

def extract_subtitle(mkv_path, track_id, output_path):
    """Extracts a subtitle track using mkvextract."""
    try:
        subprocess.run(
            ["mkvextract", str(mkv_path), "tracks", f"{track_id}:{output_path}"],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Extracted track {track_id} to {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitle: {e.stderr}")
        return False

def add_subtitle(mkv_path, sub_path, output_path, language=None):
    """Adds a subtitle file to an MKV using mkvmerge."""
    cmd = ["mkvmerge", "-o", str(output_path), str(mkv_path)]
    if language:
        cmd += ["--language", f"0:{language}"]
    cmd += [str(sub_path)]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Created modified MKV: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error adding subtitle: {e.stderr}")
        return False

def remove_subtitle(mkv_path, track_id, output_path):
    """Removes a subtitle track by excluding it via mkvmerge."""
    # To remove a track in mkvmerge, we specify the tracks we want to KEEP.
    # However, mkvmerge has --subtitle-tracks which can exclude tracks if prefixed with !.
    # But usually it's easier to use --no-subtitles or --subtitle-tracks with IDs.
    
    # Let's get all tracks and exclude the one we want to remove.
    info = get_mkv_info(mkv_path)
    if not info:
        return False
    
    tracks_to_keep = []
    for track in info.get("tracks", []):
        if track["id"] != track_id:
            # We want to keep this track. But mkvmerge --audio-tracks etc. takes IDs of tracks PER FILE.
            # Actually, mkvmerge -o out.mkv --subtitle-tracks !ID in.mkv is often used.
            pass

    # Easier way: mkvmerge -o out.mkv --subtitle-tracks !track_id mkv_path
    cmd = ["mkvmerge", "-o", str(output_path), "--subtitle-tracks", f"!{track_id}", str(mkv_path)]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Removed track {track_id}, created: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error removing subtitle: {e.stderr}")
        return False

def clean_subtitle(sub_path, output_path):
    """Cleans up subtitle tags and formatting using pysubs2."""
    try:
        subs = pysubs2.load(str(sub_path))
        for line in subs:
            # Use plaintext to strip tags
            line.text = line.plaintext
        subs.save(str(output_path))
        print(f"Cleaned subtitle saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error cleaning subtitle: {e}")
        return False

def get_modified_path(original_path, suffix="-mod"):
    p = Path(original_path)
    return p.parent / f"{p.stem}{suffix}{p.suffix}"

def list_subtitle_tracks(mkv_path):
    info = get_mkv_info(mkv_path)
    if not info:
        return []
    
    sub_tracks = []
    for track in info.get("tracks", []):
        if track["type"] == "subtitles":
            lang = track.get("properties", {}).get("language", "und")
            codec = track.get("codec", "unknown")
            sub_tracks.append({"id": track["id"], "language": lang, "codec": codec})
    return sub_tracks

def main():
    while True:
        print("\n--- MKV Subtitle Tools ---")
        print("1. Extract subtitle from MKV")
        print("2. Add subtitle to MKV")
        print("3. Remove subtitle from MKV")
        print("4. Clean up subtitle (remove tags/formatting)")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "5":
            break
        
        if choice == "1":
            mkv_path = input("Enter path to MKV file: ").strip()
            if not os.path.exists(mkv_path):
                print("File not found.")
                continue
            
            tracks = list_subtitle_tracks(mkv_path)
            if not tracks:
                print("No subtitle tracks found in this MKV.")
                continue
            
            print("Subtitle tracks:")
            for t in tracks:
                print(f"  ID {t['id']}: {t['language']} ({t['codec']})")
            
            try:
                track_id = int(input("Enter Track ID to extract: "))
                output_path = get_modified_path(mkv_path).with_suffix(".srt")
                extract_subtitle(mkv_path, track_id, output_path)
            except ValueError:
                print("Invalid track ID.")
        
        elif choice == "2":
            mkv_path = input("Enter path to MKV file: ").strip()
            sub_path = input("Enter path to subtitle file (.srt/.ass): ").strip()
            if not os.path.exists(mkv_path) or not os.path.exists(sub_path):
                print("One or more files not found.")
                continue
            
            lang = input("Enter language code (e.g. eng, optional): ").strip() or None
            output_path = get_modified_path(mkv_path)
            add_subtitle(mkv_path, sub_path, output_path, lang)
            
        elif choice == "3":
            mkv_path = input("Enter path to MKV file: ").strip()
            if not os.path.exists(mkv_path):
                print("File not found.")
                continue
                
            tracks = list_subtitle_tracks(mkv_path)
            if not tracks:
                print("No subtitle tracks found.")
                continue
                
            print("Subtitle tracks:")
            for t in tracks:
                print(f"  ID {t['id']}: {t['language']} ({t['codec']})")
                
            try:
                track_id = int(input("Enter Track ID to remove: "))
                output_path = get_modified_path(mkv_path)
                remove_subtitle(mkv_path, track_id, output_path)
            except ValueError:
                print("Invalid track ID.")
                
        elif choice == "4":
            sub_path = input("Enter path to subtitle file: ").strip()
            if not os.path.exists(sub_path):
                print("File not found.")
                continue
            
            output_path = get_modified_path(sub_path)
            clean_subtitle(sub_path, output_path)
            
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
