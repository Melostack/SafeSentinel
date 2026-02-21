import os
import httpx
import asyncio
from dotenv import load_dotenv

async def check_keys():
    load_dotenv()
    gemini_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    print(f"--- Diagnóstico de Chaves ---")
    
    # 1. Testar Gemini
    if gemini_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        payload = {"contents": [{"parts": [{"text": "Oi"}]}]}
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(url, json=payload)
                print(f"Gemini: {res.status_code} ({'OK' if res.status_code == 200 else res.text[:50]})")
            except Exception as e:
                print(f"Gemini: ERRO ({e})")

    # 2. Testar Groq
    if groq_key:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {groq_key}"}
        payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "Oi"}]}
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(url, headers=headers, json=payload)
                print(f"Groq: {res.status_code} ({'OK' if res.status_code == 200 else res.text[:50]})")
            except Exception as e:
                print(f"Groq: ERRO ({e})")

    # 3. Testar OpenRouter
    if openrouter_key:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {openrouter_key}"}
        payload = {"model": "meta-llama/llama-3.1-70b-instruct", "messages": [{"role": "user", "content": "Oi"}]}
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(url, headers=headers, json=payload)
                print(f"OpenRouter: {res.status_code} ({'OK' if res.status_code == 200 else res.text[:50]})")
            except Exception as e:
                print(f"OpenRouter: ERRO ({e})")

if __name__ == "__main__":
    asyncio.run(check_keys())
