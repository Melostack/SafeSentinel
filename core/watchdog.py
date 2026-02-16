import asyncio
import os
import httpx
from datetime import datetime
from dotenv import load_dotenv
from core.connectors.supabase_connector import SupabaseConnector
from core.gatekeeper import Gatekeeper
from core.humanizer import Humanizer

load_dotenv()

class SentinelWatchdog:
    """
    On-Chain Watchdog: Vigia as carteiras registradas e avisa sobre riscos.
    """
    def __init__(self):
        self.supabase = SupabaseConnector()
        self.gatekeeper = Gatekeeper()
        self.humanizer = Humanizer()
        self.check_interval = 600 # 10 minutos entre scans

    async def start_monitoring(self):
        print("🛡️ Sentinel Watchdog Ativo. Monitorando a rede...")
        while True:
            try:
                # 1. Buscar carteiras ativas no banco
                wallets = self._get_active_wallets()
                if not wallets:
                    await asyncio.sleep(60)
                    continue

                for wallet in wallets:
                    print(f"DEBUG: Escaneando carteira {wallet['address']} ({wallet['network']})...")
                    # TODO: Integrar com API de Explorer (Etherscan/Alchemy) 
                    # para pegar as transações das últimas 24h
                    
                    # Simulação de detecção de transação de risco
                    # Se transação detectada -> analisar -> notificar via Telegram
                    pass

                await asyncio.sleep(self.check_interval)
            except Exception as e:
                print(f"Erro no Watchdog: {e}")
                await asyncio.sleep(60)

    def _get_active_wallets(self):
        if not self.supabase.client: return []
        try:
            res = (self.supabase.client.schema("safetransfer")
                .table("monitored_wallets")
                .select("*")
                .eq("is_active", True)
                .execute())
            return res.data
        except: return []

if __name__ == "__main__":
    watchdog = SentinelWatchdog()
    # asyncio.run(watchdog.start_monitoring())
