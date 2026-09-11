from google import genai
from google.genai import types

def generate_ai_response(client: genai.Client, prompt: str, target_language: str, enable_search: bool) -> str:
    """Generates an answer using Gemini 2.5 Flash and provides it in the requested language."""
    config = None
    if enable_search:
        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )

    # Instruct model on the exact requested language
    system_prompt = (
        f"Answer the user query accurately. "
        f"Output your final response strictly in the {target_language} language. "
        f"If the selected language is not English, ensure natural, high-quality translation and phrasing."
    )
    
    full_prompt = f"{system_prompt}\n\nUser Question: {prompt}"

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=full_prompt,
        config=config
    )
    return response.text or "No response generated."