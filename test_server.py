import asyncio
from api.server import app

async def main():
    print("Server can be imported successfully.")

if __name__ == "__main__":
    asyncio.run(main())
