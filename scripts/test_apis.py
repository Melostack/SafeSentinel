import os
import httpx
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()

async def test_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/getMe"
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url)
            if r.status_code == 200:
                print(f"✅ Telegram: OK ({r.json()['result']['username']})")
            else:
                print(f"❌ Telegram: FAILED ({r.status_code}) {r.text}")
        except Exception as e:
            print(f"❌ Telegram: ERROR {e}")

async def test_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    # Test checking for a specific table request
    async with httpx.AsyncClient() as client:
        try:
            # We try to select from maria_prompts which is likely public-readable if RLS allows
            r = await client.get(f"{url}/rest/v1/maria_prompts?select=*", headers={"apikey": key, "Authorization": f"Bearer {key}"})
            if r.status_code in [200, 204]:
                print(f"✅ Supabase: OK (Table Access)")
            else:
                print(f"❌ Supabase: FAILED ({r.status_code}) {r.text}")
        except Exception as e:
            print(f"❌ Supabase: ERROR {e}")

async def test_binance():
    # Public request is enough to check if API is alive, but we can check a simple restricted one
    # Actually just check connectivity
    url = "https://api.binance.com/api/v3/ping"
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url)
            # Binance might return 451 based on region, but we can treat 200 or 451 as 'Alive' but restricted
            if r.status_code == 200:
                print(f"✅ Binance Connectivity: OK")
            elif r.status_code == 451:
                print(f"⚠️ Binance Connectivity: OK (Restricted by Region 451)")
            else:
                print(f"❌ Binance Connectivity: FAILED ({r.status_code})")
        except Exception as e:
            print(f"❌ Binance Connectivity: ERROR {e}")

async def test_perplexity():
    key = os.getenv("PERPLEXITY_API_KEY")
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": "hello"}],
        "max_tokens": 10
    }
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url, headers=headers, json=payload, timeout=20.0)
            if r.status_code == 200:
                print(f"✅ Perplexity: OK")
            else:
                print(f"❌ Perplexity: FAILED ({r.status_code}) {r.text}")
        except Exception as e:
            print(f"❌ Perplexity: ERROR {e}")

async def test_cmc():
    key = os.getenv("CMC_API_KEY")
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC"
    headers = {"X-CMC_PRO_API_KEY": key}
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url, headers=headers)
            if r.status_code == 200:
                print(f"✅ CMC: OK")
            else:
                print(f"❌ CMC: FAILED ({r.status_code}) {r.text}")
        except Exception as e:
            print(f"❌ CMC: ERROR {e}")

async def test_google():
    key = os.getenv("GOOGLE_API_KEY")
    # Using gemini-2.0-flash as verified by ListModels
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": "hello"}]}]}
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url, json=payload, timeout=20.0)
            if r.status_code == 200:
                print(f"✅ Google Gemini: OK")
            else:
                print(f"❌ Google Gemini: FAILED ({r.status_code}) {r.text}")
        except Exception as e:
            print(f"❌ Google Gemini: ERROR {e}")

async def test_groq():
    key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "hello"}],
        "max_tokens": 10
    }
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url, headers=headers, json=payload, timeout=20.0)
            if r.status_code == 200:
                print(f"✅ Groq: OK")
            else:
                print(f"❌ Groq: FAILED ({r.status_code}) {r.text}")
        except Exception as e:
            print(f"❌ Groq: ERROR {e}")

async def test_openrouter():
    key = os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "user", "content": "hello"}],
        "max_tokens": 10
    }
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url, headers=headers, json=payload, timeout=20.0)
            if r.status_code == 200:
                print(f"✅ OpenRouter: OK")
            else:
                print(f"❌ OpenRouter: FAILED ({r.status_code}) {r.text}")
        except Exception as e:
            print(f"❌ OpenRouter: ERROR {e}")

async def main():
    print("--- STARTING API TESTS ---")
    await asyncio.gather(
        test_telegram(),
        test_supabase(),
        test_binance(),
        test_perplexity(),
        test_cmc(),
        test_google(),
        test_groq(),
        test_openrouter()
    )
    print("--- TESTS COMPLETED ---")

if __name__ == "__main__":
    asyncio.run(main())
