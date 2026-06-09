# SonicWeave: AI Music Curator & Burner

SonicWeave is an open-source AI tool that curates music based on your natural language requests and "burns" it directly to your USB drive or SD card.

## Features
- **Natural Language Curation:** "I want 30 minutes of upbeat chillhop for a road trip."
- **Automatic Drive Detection:** Automatically identifies removable USB/SD storage.
- **Smart Capacity Calculation:** Tells you exactly how many songs can fit on your device.
- **High-Speed Transfer:** Concurrent downloading and burning for maximum efficiency.
- **Library Management:** List and delete existing songs on your drive.
- **Legal & Free:** Uses the Jamendo API for free, royalty-free music.

## Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/Pkkarthik12/SonicWeave.git
   cd SonicWeave
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup
1. Get a **FREE** Gemini API key from [Google AI Studio](https://aistudio.google.com/).
2. Get a **FREE** Jamendo Client ID from [Jamendo Developer Portal](https://developer.jamendo.com/v3.0).
3. Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_key
   JAMENDO_CLIENT_ID=your_jamendo_id
   ```

## Usage
Run the program:
```bash
python -m sonicweave.main
```

## License
MIT
