import re
import requests
from google import genai

def extract_search_keyword(client: genai.Client, current_prompt: str, history: list) -> str:
    """Uses past chat turns to resolve pronouns like 'it', 'this', or 'that' into a specific noun."""
    ambiguous_words = {"it", "this", "that", "them", "these", "its", "here", "there"}
    prompt_tokens = set(re.findall(r'\b\w+\b', current_prompt.lower()))
    
    # If the user used a pronoun and we have prior chat history, use Gemini to identify the entity
    if prompt_tokens.intersection(ambiguous_words) and history:
        context_snippets = []
        for msg in history[-4:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            context_snippets.append(f"{role}: {msg['content'][:140]}")
        conversation_context = "\n".join(context_snippets)

        resolution_prompt = (
            "Given this conversation history and the user's latest query, "
            "identify the exact object/person/place the user wants an image of. "
            "Return ONLY 1 to 3 words naming that specific subject. Do not write full sentences.\n\n"
            f"History:\n{conversation_context}\n\n"
            f"Query: {current_prompt}\n"
            "Subject:"
        )
        try:
            res = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=resolution_prompt
            )
            entity = res.text.strip().strip('"\'')
            if entity and len(entity.split()) <= 4:
                return entity
        except Exception:
            pass

    # Strip filler command words if no resolution was needed
    cleaned = re.sub(r'(?i)\b(give|show|the|image|of|photo|picture|look|like|please|can|you)\b', '', current_prompt)
    cleaned = re.sub(r'[^\w\s]', '', cleaned).strip()
    return " ".join(cleaned.split()[:3])


def fetch_related_image(client: genai.Client, query: str, history: list):
    """Fetches a thumbnail from Wikipedia. Returns metadata dict or None."""
    search_term = extract_search_keyword(client, query, history)
    
    # Do not execute empty or raw pronoun queries
    if not search_term or search_term.lower() in {"it", "this", "that", "them"}:
        return None

    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": search_term,
            "gsrlimit": 1,
            "prop": "pageimages|extracts",
            "pithumbsize": 600,
            "exintro": True,
            "explaintext": True,
            "exchars": 140
        }
        headers = {"User-Agent": "GeminiStreamlitBot/1.0 (contact@example.com)"}
        res = requests.get(url, params=params, headers=headers, timeout=5)
        data = res.json()
        
        pages = data.get("query", {}).get("pages", {})
        if pages:
            first_page = next(iter(pages.values()))
            image_url = first_page.get("thumbnail", {}).get("source")
            title = first_page.get("title", "")
            description = first_page.get("extract", "")
            
            if image_url:
                return {"url": image_url, "title": title, "desc": description}
    except Exception:
        pass
    
    return None