import os
import psutil
import shutil
from rich.console import Console
from rich.table import Table

console = Console()

def get_removable_drives():
    """
    Detects and returns a list of removable drives (USB/SD).
    """
    removable_drives = []
    for partition in psutil.disk_partitions(all=False):
        if 'removable' in partition.opts.lower() or 'cdrom' in partition.opts.lower():
            try:
                usage = shutil.disk_usage(partition.mountpoint)
                removable_drives.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free
                })
            except (PermissionError, OSError):
                continue
    return removable_drives

def format_size(bytes_size):
    """
    Helper to format bytes into a human-readable string.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

def list_songs_on_drive(mountpoint):
    """
    Lists all .mp3 files on the specified drive.
    """
    songs = []
    for root, dirs, files in os.walk(mountpoint):
        for file in files:
            if file.lower().endswith(".mp3"):
                songs.append(os.path.join(root, file))
    return songs

def delete_songs(songs_to_delete):
    """
    Deletes a list of file paths.
    """
    for song in songs_to_delete:
        try:
            os.remove(song)
        except Exception as e:
            console.print(f"[red]Error deleting {song}: {e}[/red]")
