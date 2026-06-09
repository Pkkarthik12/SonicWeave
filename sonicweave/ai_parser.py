import json
from google import genai

def parse_music_request(prompt, api_key):
    """
    Uses Gemini to extract Jamendo API parameters from a user's prompt.
    """
    client = genai.Client(api_key=api_key)
    
    system_instruction = """
    You are a music curator for SonicWeave. Your job is to extract search parameters for the Jamendo Music API from user requests.
    Output ONLY a JSON object with these keys:
    - tags: (string) Comma-separated genres or moods (e.g., 'rock,upbeat').
    - fuzzytags: (string) Similar to tags but for broader search.
    - limit: (int) Number of songs requested (default 10).
    - speed: (string) 'verylow', 'low', 'medium', 'high', 'veryhigh' (optional).
    """
    
    try:
        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=f"{system_instruction}\nUser Request: {prompt}"
        )
        
        # Clean up JSON if LLM added markdown blocks
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_text)
    except Exception as e:
        # Fallback: if AI fails, use the raw prompt as a tag
        return {"tags": prompt.strip().replace(" ", ","), "limit": 10}
