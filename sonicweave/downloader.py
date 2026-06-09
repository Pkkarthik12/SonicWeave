import requests
import os
import concurrent.futures
from rich.progress import Progress

def search_jamendo(params, client_id):
    """
    Searches Jamendo for tracks matching the parameters.
    """
    base_url = "https://api.jamendo.com/v3.0/tracks/"
    query_params = {
        "client_id": client_id,
        "format": "json",
        "hasdescription": 1,
        "audioformat": "mp32", # High quality mp3
        "limit": params.get("limit", 10),
        "tags": params.get("tags"),
        "fuzzytags": params.get("fuzzytags"),
        "speed": params.get("speed"),
        "order": "popularity_total"
    }
    
    response = requests.get(base_url, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def download_track(track, destination_folder, progress, task_id):
    """
    Downloads a single track to the destination.
    """
    url = track.get("audio")
    name = f"{track.get('artist_name')} - {track.get('name')}.mp3".replace("/", "_").replace("\\", "_")
    file_path = os.path.join(destination_folder, name)
    
    if not url:
        return False
        
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            progress.update(task_id, total=total_size)
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress.update(task_id, advance=len(chunk))
            return True
    except Exception:
        return False
    return False

def download_tracks_concurrently(tracks, dest_folder):
    """
    Downloads multiple tracks at once using a thread pool.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        
    with Progress() as progress:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for track in tracks:
                name = f"{track.get('artist_name')} - {track.get('name')}"
                task_id = progress.add_task(f"[cyan]Downloading {name[:30]}...", total=None)
                futures.append(executor.submit(download_track, track, dest_folder, progress, task_id))
            
            concurrent.futures.wait(futures)
