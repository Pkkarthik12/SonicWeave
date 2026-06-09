import os
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

from .storage_utils import get_removable_drives, format_size, list_songs_on_drive, delete_songs
from .ai_parser import parse_music_request
from .downloader import search_jamendo, download_tracks_concurrently

load_dotenv()
console = Console()

def main():
    console.print(Panel("[bold magenta]SonicWeave: AI Music Curator & Burner[/bold magenta]", subtitle="Open Source & Fast"))
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    jamendo_id = os.getenv("JAMENDO_CLIENT_ID")
    
    if not gemini_key or not jamendo_id:
        console.print("[red]Error:[/red] GEMINI_API_KEY or JAMENDO_CLIENT_ID not found in .env file.")
        sys.exit(1)

    # 1. Detect Drives
    drives = get_removable_drives()
    if not drives:
        console.print("[yellow]No removable drives detected. Please plug in a USB or SD card.[/yellow]")
        if not Confirm.ask("Continue anyway (using current directory)?"):
            sys.exit(0)
        selected_drive = {"mountpoint": ".", "free": 10**12, "device": "Local Folder"}
    else:
        table = Table(title="Detected Removable Storage")
        table.add_column("ID", style="cyan")
        table.add_column("Device", style="magenta")
        table.add_column("Mount Point", style="green")
        table.add_column("Free Space", style="yellow")
        
        for i, d in enumerate(drives):
            table.add_row(str(i+1), d['device'], d['mountpoint'], format_size(d['free']))
        
        console.print(table)
        choice = int(Prompt.ask("Select drive ID", choices=[str(i+1) for i in range(len(drives))]))
        selected_drive = drives[choice-1]

    console.print(f"\n[bold green]Targeting Drive:[/bold green] {selected_drive['device']} ({selected_drive['mountpoint']})")
    
    # 2. List Existing Music & Manage Space
    existing_songs = list_songs_on_drive(selected_drive['mountpoint'])
    if existing_songs:
        console.print(f"Found [bold blue]{len(existing_songs)}[/bold blue] existing songs on the drive.")
        if Confirm.ask("Would you like to see the list or delete some songs?"):
            for i, s in enumerate(existing_songs):
                console.print(f"{i+1}. {os.path.basename(s)}")
            
            if Confirm.ask("Delete all existing songs to make room?"):
                delete_songs(existing_songs)
                console.print("[green]Space cleared![/green]")
                selected_drive['free'] = 10**12 # Reset local free space estimate (simplified)

    # 3. AI Curation Request
    user_prompt = Prompt.ask("\n[bold cyan]What kind of music would you like to burn today?[/bold cyan]\n(e.g., '50 upbeat electronic songs' or 'chill jazz for study')")
    
    with console.status("[bold green]AI is curating your playlist...[/bold green]"):
        api_params = parse_music_request(user_prompt, gemini_key)
    
    console.print(f"AI suggested: [yellow]{api_params.get('tags', 'mixed')}[/yellow] with limit [yellow]{api_params.get('limit', 10)}[/yellow]")
    
    # 4. Search and Capacity Check
    with console.status("[bold green]Searching Jamendo catalog...[/bold green]"):
        tracks = search_jamendo(api_params, jamendo_id)
    
    if not tracks:
        console.print("[red]No tracks found matching your request.[/red]")
        sys.exit(1)
        
    estimated_size = len(tracks) * 5 * 1024 * 1024 # Est 5MB per song
    if estimated_size > selected_drive['free']:
        console.print(f"[red]Not enough space![/red] Needs ~{format_size(estimated_size)}, but only {format_size(selected_drive['free'])} free.")
        tracks = tracks[:int(selected_drive['free'] // (5 * 1024 * 1024))]
        console.print(f"Reducing batch to [bold]{len(tracks)}[/bold] songs.")

    console.print(f"Ready to download and burn [bold green]{len(tracks)}[/bold green] tracks.")
    if Confirm.ask("Start burning?"):
        # Create a music folder on the drive
        music_folder = os.path.join(selected_drive['mountpoint'], "SonicWeave_Music")
        download_tracks_concurrently(tracks, music_folder)
        console.print(f"\n[bold green]Success![/bold green] All songs burned to [cyan]{music_folder}[/cyan].")
        console.print("Safely eject your drive and enjoy the music!")

if __name__ == "__main__":
    main()
