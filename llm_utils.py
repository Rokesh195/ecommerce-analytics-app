import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(prompt, context=None):
    data = {
        "model": "mistral", 
        "prompt": prompt,
        "stream": False
    }
    if context:
        data["context"] = context
    resp = requests.post(OLLAMA_URL, json=data)
    if resp.ok:
        return resp.json().get("response", "")
    else:
        return "LLM error"
