"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldCheck, ShieldAlert, Search, Cpu, 
  Globe, Zap, ArrowRight, Info, ExternalLink, X, TrendingUp, BarChart3, Clock
} from 'lucide-react';

export default function SafeSentinelDashboard() {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState<'sentinel' | 'discovery'>('sentinel');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [parsedIntent, setIntent] = useState<any>(null);
  const [showIntel, setShowIntel] = useState(false);

  const handleProcess = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      const apiUrl = '/api-engine';
      
      if (mode === 'sentinel') {
        const intentResponse = await fetch(`${apiUrl}/extract`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: query })
        });
        const intent = await intentResponse.json();
        setIntent(intent);

        const checkResponse = await fetch(`${apiUrl}/check`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            asset: intent.asset || 'USDT',
            origin: intent.origin || 'Binance',
            destination: intent.destination || 'MetaMask',
            network: intent.network || 'ERC20',
            address: intent.address || "0x0000000000000000000000000000000000000000"
          })
        });
        
        const data = await checkResponse.json();
        setResult({ ...data, type: 'sentinel' });
      } else {
        const [asset, ...networkParts] = query.split(' ');
        const network = networkParts.join(' ') || 'Mainnet';

        const findResponse = await fetch(`${apiUrl}/find`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ asset, network })
        });
        const data = await findResponse.json();
        setResult({ ...data, type: 'discovery' });
      }
    } catch (error) {
      setResult({
        risk_level: 'CRITICAL',
        title: 'Erro de Conexão',
        message: 'O motor SafeSentinel está fora de alcance. Tente novamente mais tarde.'
      });
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val);
  };

  return (
    <div className="min-h-screen bg-[#020202] text-white selection:bg-cyan-500/30 font-sans flex flex-col items-center p-8 overflow-x-hidden">
      {/* Dynamic Background */}
      <div className="fixed inset-0 pointer-events-none opacity-20">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-cyan-500 blur-[120px] rounded-full animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[400px] h-[400px] bg-purple-500 blur-[120px] rounded-full animate-pulse" />
      </div>

      {/* Smart Trust Panel */}
      <AnimatePresence>
        {showIntel && result?.token_intel && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowIntel(false)}
              className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
            />
            <motion.div 
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed top-0 right-0 h-full w-full max-w-md bg-[#0A0A0A]/80 backdrop-blur-3xl border-l border-white/10 z-50 p-8 shadow-2xl flex flex-col"
            >
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 overflow-hidden">
                    <img src={result.token_intel.logo} alt="" className="w-6 h-6 rounded-full" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">{result.token_intel.name}</h3>
                    <span className="text-[10px] font-bold text-white/30 uppercase tracking-widest">{result.token_intel.symbol} Metadata</span>
                  </div>
                </div>
                <button onClick={() => setShowIntel(false)} className="p-2 hover:bg-white/5 rounded-full transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-6 flex-grow overflow-y-auto pr-2 custom-scrollbar">
                <div className="p-6 rounded-3xl bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-white/5">
                  <span className="text-[10px] font-bold text-white/40 uppercase block mb-4">Trust Score Algorithm v1.0</span>
                  <div className="flex items-end gap-2">
                    <span className="text-6xl font-black tracking-tighter">{result.trust_score}</span>
                    <span className="text-xl font-bold text-white/20 mb-2">/ 100</span>
                  </div>
                  <div className="mt-4 h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${result.trust_score}%` }}
                      className="h-full bg-gradient-to-r from-cyan-500 to-purple-500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                    <TrendingUp className="w-4 h-4 text-cyan-400 mb-2" />
                    <span className="text-[10px] font-bold text-white/30 uppercase block mb-1">Market Cap</span>
                    <span className="text-sm font-bold">{formatCurrency(result.token_intel.market_cap)}</span>
                  </div>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                    <BarChart3 className="w-4 h-4 text-purple-400 mb-2" />
                    <span className="text-[10px] font-bold text-white/30 uppercase block mb-1">Vol (24h)</span>
                    <span className="text-sm font-bold">{formatCurrency(result.token_intel.volume_24h)}</span>
                  </div>
                </div>

                <div className="p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4">
                  <div className="flex items-center gap-3">
                    <Clock className="w-4 h-4 text-white/20" />
                    <div className="flex-grow">
                      <span className="text-[10px] font-bold text-white/30 uppercase block">Token Age</span>
                      <span className="text-sm">Since {new Date(result.token_intel.date_added).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <ShieldCheck className="w-4 h-4 text-white/20" />
                    <div className="flex-grow">
                      <span className="text-[10px] font-bold text-white/30 uppercase block">Contracts</span>
                      <span className="text-sm">{result.token_intel.contracts?.length || 0} Networks Verified</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <span className="text-[10px] font-bold text-white/30 uppercase block">Official Resources</span>
                  <div className="grid grid-cols-2 gap-2">
                    {result.token_intel.official_links?.website?.[0] && (
                      <a href={result.token_intel.official_links.website[0]} target="_blank" className="p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 text-[11px] font-bold flex items-center justify-between group">
                        WEBSITE <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-3xl z-10"
      >
        {/* Top Branding */}
        <div className="flex flex-col items-center mb-12">
          <div className="px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-xl flex items-center gap-2 mb-6">
            <Zap className="w-3.5 h-3.5 text-cyan-400 fill-cyan-400" />
            <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-white/70">Melostack Sentinel Engine</span>
          </div>
          <h1 className="text-5xl font-black tracking-tighter mb-2 bg-gradient-to-b from-white to-white/40 bg-clip-text text-transparent">
            SafeSentinel
          </h1>
          <p className="text-white/40 font-medium text-center">The Web3 Interpretive Security Layer</p>
        </div>

        {/* Command Center Bar */}
        <div className="relative group mb-12">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-[28px] blur opacity-25 group-focus-within:opacity-100 transition-all duration-500" />
          <div className="relative bg-[#0A0A0A] border border-white/10 rounded-[24px] p-2 flex items-center gap-4 shadow-2xl backdrop-blur-2xl">
            <div className="pl-4">
              <Search className="w-5 h-5 text-white/20" />
            </div>
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={mode === 'sentinel' ? "Ex: Mandar USDT da OKX pra Binance via Polygon..." : "Ex: OKB X-Layer"}
              className="flex-grow bg-transparent border-none py-4 text-lg focus:outline-none placeholder:text-white/10 font-medium"
              onKeyDown={(e) => e.key === 'Enter' && handleProcess()}
            />
            <button 
              onClick={handleProcess}
              disabled={loading || query.length < 2}
              className="bg-white text-black px-6 py-3 rounded-[18px] font-bold text-sm hover:scale-[1.02] active:scale-95 transition-all disabled:opacity-30 disabled:scale-100"
            >
              {loading ? "Analizando..." : "Verificar"}
            </button>
          </div>
        </div>

        {/* Mode Toggles */}
        <div className="flex gap-4 mb-8 justify-center">
          <button 
            onClick={() => { setMode('sentinel'); setResult(null); }}
            className={`px-6 py-2 rounded-full border text-xs font-bold transition-all ${mode === 'sentinel' ? 'bg-white text-black border-white' : 'border-white/10 text-white/40 hover:bg-white/5'}`}
          >
            MODO SENTINEL
          </button>
          <button 
            onClick={() => { setMode('discovery'); setResult(null); }}
            className={`px-6 py-2 rounded-full border text-xs font-bold transition-all ${mode === 'discovery' ? 'bg-white text-black border-white' : 'border-white/10 text-white/40 hover:bg-white/5'}`}
          >
            MODO DISCOVERY
          </button>
        </div>

        {/* Result UI */}
        <AnimatePresence mode='wait'>
          {result && result.type === 'sentinel' && (
            <motion.div 
              key="sentinel-result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className={`p-8 rounded-[32px] border backdrop-blur-3xl shadow-3xl ${
                result.risk_level === 'LOW' ? 'bg-green-500/5 border-green-500/20' : 
                result.risk_level === 'MEDIUM' ? 'bg-yellow-500/5 border-yellow-500/20' : 
                'bg-red-500/5 border-red-500/20'
              }`}>
                <div className="flex items-start gap-6">
                  <div className={`p-4 rounded-2xl ${
                    result.risk_level === 'LOW' ? 'bg-green-500/20 text-green-400' : 
                    result.risk_level === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400' : 
                    'bg-red-500/20 text-red-400'
                  }`}>
                    {result.risk_level === 'LOW' ? <ShieldCheck className="w-8 h-8" /> : <ShieldAlert className="w-8 h-8" />}
                  </div>
                  <div className="flex-grow">
                    <div className="flex items-center justify-between mb-3">
                      <h2 className="text-2xl font-bold">{result.title}</h2>
                      {result.trust_score > 0 && (
                        <button 
                          onClick={() => setShowIntel(true)}
                          className="px-3 py-1 rounded-full bg-white/5 border border-white/10 flex items-center gap-2 hover:bg-white/10 transition-all group"
                        >
                          <span className="text-[10px] font-bold text-white/40 group-hover:text-white transition-colors">TRUST SCORE</span>
                          <span className={`text-[10px] font-black ${result.trust_score > 70 ? 'text-green-400' : result.trust_score > 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                            {result.trust_score}
                          </span>
                        </button>
                      )}
                    </div>
                    <p className="text-white/70 leading-relaxed mb-6 italic">"{result.message}"</p>
                    
                    <div className="flex items-center gap-4 py-4 border-t border-white/5">
                      <div className="flex items-center gap-2 px-3 py-1 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
                        <Cpu className="w-3 h-3 text-cyan-400" />
                        <span className="text-[10px] font-bold text-cyan-400 uppercase">RPC Verified</span>
                      </div>
                      <div className="text-[11px] text-white/30 font-medium">
                        {result.on_chain?.type} • Network: {parsedIntent?.network}
                      </div>
                      <a 
                        href={result.on_chain?.explorer_url} 
                        target="_blank" 
                        className="ml-auto text-[11px] font-bold text-white/40 hover:text-white flex items-center gap-1"
                      >
                        EXPLORER <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {result && result.type === 'discovery' && (
            <motion.div 
              key="discovery-result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="p-8 rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-3xl shadow-3xl">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                  <Globe className="w-6 h-6 text-cyan-400" />
                  Rota de Liquidez: {query.split(' ')[0].toUpperCase()}
                </h2>
                
                <div className="space-y-4">
                  {result.data.steps?.map((step: string, i: number) => (
                    <div key={i} className="flex gap-4 items-center">
                      <div className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-[10px] font-bold">
                        {i + 1}
                      </div>
                      <p className="text-white/80 text-sm">{step}</p>
                    </div>
                  ))}
                </div>

                <div className="mt-8 grid grid-cols-2 gap-4">
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                    <span className="text-[10px] font-bold text-white/30 uppercase block mb-1">Melhor CEX</span>
                    <span className="text-sm font-medium">{result.data.cex_source}</span>
                  </div>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                    <span className="text-[10px] font-bold text-white/30 uppercase block mb-1">Bridge Recomendada</span>
                    <span className="text-sm font-medium">{result.data.recommended_bridge || 'Nativa'}</span>
                  </div>
                </div>

                {result.data.warning && (
                  <div className="mt-6 p-4 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex gap-3 items-center">
                    <Info className="w-4 h-4 text-yellow-400" />
                    <p className="text-xs text-yellow-400/80">{result.data.warning}</p>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <footer className="mt-20 flex flex-col items-center gap-4">
          <div className="flex gap-8 opacity-20 hover:opacity-50 transition-opacity">
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4" />
              <span className="text-[10px] font-bold uppercase tracking-widest">Global Discovery</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4" />
              <span className="text-[10px] font-bold uppercase tracking-widest">On-Chain Forensic</span>
            </div>
          </div>
          <p className="text-[10px] font-mono text-white/10 uppercase tracking-[0.4em]">
            Powered by vibe-to-code Protocol
          </p>
        </footer>
      </motion.div>
    </div>
  );
}
