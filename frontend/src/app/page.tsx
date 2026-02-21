"use client";

import React, { useState, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from 'next/image';
import { 
  ShieldCheck, ShieldAlert, Search, Cpu, 
  Globe, Zap, Info, ExternalLink, X, TrendingUp, BarChart3, 
  Lock, Unlock, AlertTriangle, Fingerprint, Activity, MousePointer2, ChevronUp
} from 'lucide-react';

// Componentes Memoizados para Performance
const TrustGauge = React.memo(({ score }: { score: number }) => {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = useMemo(() => circumference - (score / 100) * circumference, [score, circumference]);
  const color = useMemo(() => score > 70 ? '#22c55e' : score > 40 ? '#eab308' : '#ef4444', [score]);

  return (
    <div className="relative flex items-center justify-center w-28 h-28 sm:w-32 sm:h-32">
      <svg className="w-full h-full transform -rotate-90">
        <circle cx="50%" cy="50%" r={radius} stroke="currentColor" strokeWidth="8" fill="transparent" className="text-white/5" />
        <motion.circle 
          cx="50%" cy="50%" r={radius} stroke={color} strokeWidth="8" fill="transparent" 
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-2xl sm:text-3xl font-black">{score}</span>
        <span className="text-[7px] sm:text-[8px] font-bold text-white/30 tracking-[0.2em]">SCORE</span>
      </div>
    </div>
  );
});

TrustGauge.displayName = 'TrustGauge';

const MetricCard = React.memo(({ label, active, danger, warning, success, icon }: any) => (
  <div className={`p-4 sm:p-5 rounded-2xl border backdrop-blur-xl flex flex-col items-center gap-3 transition-all active:scale-95 cursor-default ${
    active ? (danger ? 'bg-red-500/10 border-red-500/30 text-red-400' : warning ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400' : 'bg-green-500/10 border-green-500/30 text-green-400') 
    : 'bg-white/5 border-white/10 text-white/20'
  }`}>
    {icon || (active ? <AlertTriangle className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4" />)}
    <span className="text-[9px] font-black uppercase tracking-widest">{label}</span>
  </div>
));

MetricCard.displayName = 'MetricCard';

export default function SafeSentinelDashboard() {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState<'sentinel' | 'discovery'>('sentinel');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [showIntel, setShowIntel] = useState(false);

  const handleProcess = useCallback(async () => {
    if (query.length < 2) return;
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
        const findResponse = await fetch(`${apiUrl}/find`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ asset: query.split(' ')[0], network: query.split(' ')[1] || 'Mainnet' })
        });
        const data = await findResponse.json();
        setResult({ ...data, type: 'discovery' });
      }
    } catch (error) {
      setResult({
        risk_level: 'CRITICAL',
        title: 'Erro de Conexão',
        message: 'O motor SafeSentinel está fora de alcance.'
      });
    } finally {
      setLoading(false);
    }
  }, [query, mode]);

  const formatCurrency = useCallback((val: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val);
  }, []);

  return (
    <div className="min-h-screen bg-[#020202] text-white selection:bg-cyan-500/30 font-sans flex flex-col items-center p-4 sm:p-12 overflow-x-hidden relative">
      {/* Premium Mesh Gradient Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-cyan-500/10 blur-[140px] rounded-full animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-purple-500/10 blur-[140px] rounded-full animate-pulse" />
      </div>

      {/* Trust Panel - Mobile Adaptive Drawer */}
      <AnimatePresence>
        {showIntel && result?.token_intel && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowIntel(false)}
              className="fixed inset-0 bg-black/80 backdrop-blur-md z-40"
            />
            <motion.div 
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed bottom-0 left-0 right-0 sm:top-0 sm:right-0 sm:left-auto sm:h-full sm:w-full sm:max-w-md bg-[#0A0A0A]/95 backdrop-blur-3xl border-t sm:border-t-0 sm:border-l border-white/10 z-50 p-6 sm:p-8 shadow-2xl rounded-t-[32px] sm:rounded-none flex flex-col max-h-[90vh] sm:max-h-none"
            >
              <div className="w-12 h-1 bg-white/10 rounded-full mx-auto mb-6 sm:hidden" />
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10 overflow-hidden relative">
                    {result.token_intel.logo && (
                      <Image 
                        src={result.token_intel.logo} 
                        alt={result.token_intel.name} 
                        fill 
                        className="object-cover rounded-full"
                      />
                    )}
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">{result.token_intel.name}</h3>
                    <span className="text-[10px] font-bold text-white/30 uppercase tracking-widest">{result.token_intel.symbol}</span>
                  </div>
                </div>
                <button onClick={() => setShowIntel(false)} className="p-2 hover:bg-white/5 rounded-full"><X /></button>
              </div>

              <div className="space-y-6 flex-grow overflow-y-auto pr-2 custom-scrollbar">
                <div className="p-6 rounded-3xl bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-white/5">
                  <span className="text-[10px] font-bold text-white/40 uppercase block mb-4">Trust Score Algorithm</span>
                  <div className="flex items-end gap-2">
                    <span className="text-6xl font-black tracking-tighter">{result.trust_score}</span>
                    <span className="text-xl font-bold text-white/20 mb-2">/ 100</span>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-center">
                    <TrendingUp className="w-4 h-4 text-cyan-400 mx-auto mb-2" />
                    <span className="text-[10px] font-bold text-white/30 uppercase block mb-1">Market Cap</span>
                    <span className="text-sm font-bold">{formatCurrency(result.token_intel.market_cap)}</span>
                  </div>
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-center">
                    <BarChart3 className="w-4 h-4 text-purple-400 mx-auto mb-2" />
                    <span className="text-[10px] font-bold text-white/30 uppercase block mb-1">Vol (24h)</span>
                    <span className="text-sm font-bold">{formatCurrency(result.token_intel.volume_24h)}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col items-center mb-12 sm:mb-16 w-full"
      >
        <div className="px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-xl flex items-center gap-2 mb-6 sm:mb-8 shadow-lg">
          <Zap className="w-3.5 h-3.5 text-cyan-400 fill-cyan-400" />
          <span className="text-[9px] sm:text-[10px] font-black tracking-[0.2em] uppercase text-white/80">Melostack Sentinel v2.0</span>
        </div>
        <h1 className="text-4xl sm:text-7xl font-black tracking-tighter mb-3 text-center bg-gradient-to-b from-white to-white/40 bg-clip-text text-transparent px-4">
          SafeSentinel
        </h1>
        <p className="text-white/30 font-bold uppercase tracking-[0.2em] text-[9px] sm:text-xs flex items-center gap-2">
          <Fingerprint className="w-3.5 h-3.5" /> Interpretive Security Layer
        </p>
      </motion.header>

      {/* Main Command Bar */}
      <div className="w-full max-w-2xl relative group mb-10 sm:mb-12">
        <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-[24px] sm:rounded-[32px] blur-lg opacity-40 group-focus-within:opacity-100 transition-all duration-500" />
        <div className="relative bg-[#0A0A0A]/80 border border-white/10 rounded-[20px] sm:rounded-[28px] p-1.5 sm:p-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-2 shadow-2xl backdrop-blur-3xl">
          <input 
            type="text" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={mode === 'sentinel' ? "Ex: Mandar USDT..." : "Ex: OKB X-Layer"}
            className="flex-grow bg-transparent border-none px-5 py-4 sm:py-5 text-base sm:text-lg focus:outline-none placeholder:text-white/10 font-semibold text-center sm:text-left"
            style={{ fontSize: '16px' }} // Fix iOS auto-zoom
            onKeyDown={(e) => e.key === 'Enter' && handleProcess()}
          />
          <button 
            onClick={handleProcess}
            disabled={loading || query.length < 2}
            className="bg-white text-black px-8 py-4 sm:py-4 rounded-[16px] sm:rounded-[22px] font-black text-xs sm:text-sm active:scale-95 transition-all disabled:opacity-20 shadow-xl"
          >
            {loading ? <Activity className="w-4 h-4 animate-spin mx-auto" /> : "VERIFICAR"}
          </button>
        </div>
      </div>

      {/* Mode Selector - Premium Tabs */}
      <div className="flex p-1 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl mb-12 sm:mb-16">
        {(['sentinel', 'discovery'] as const).map((m) => (
          <button 
            key={m}
            onClick={() => { setMode(m); setResult(null); }}
            className={`px-6 sm:px-10 py-2.5 rounded-xl text-[10px] font-black transition-all tracking-[0.1em] ${mode === m ? 'bg-white text-black shadow-lg' : 'text-white/40 hover:text-white'}`}
          >
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Dynamic Content */}
      <AnimatePresence mode='wait'>
        {result && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.98, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="w-full max-w-3xl space-y-6 sm:space-y-8"
          >
            {/* Risk Card */}
            <div className={`p-6 sm:p-10 rounded-[32px] sm:rounded-[40px] border backdrop-blur-3xl shadow-2xl relative overflow-hidden ${
              result.risk_level === 'LOW' ? 'bg-green-500/[0.03] border-green-500/20' : 
              result.risk_level === 'MEDIUM' ? 'bg-yellow-500/[0.03] border-yellow-500/20' : 
              'bg-red-500/[0.03] border-red-500/20'
            }`}>
              <div className="flex flex-col md:flex-row items-center sm:items-start gap-8 sm:gap-12">
                <div className="flex flex-col items-center gap-4">
                  <TrustGauge score={result.trust_score} />
                  <div className={`px-4 py-1.5 rounded-full text-[9px] font-black tracking-widest ${
                    result.risk_level === 'LOW' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                  }`}>
                    RISCO {result.risk_level}
                  </div>
                </div>
                <div className="flex-grow text-center sm:text-left space-y-4">
                  <h2 className="text-2xl sm:text-4xl font-black tracking-tighter leading-tight">{result.title}</h2>
                  <p className="text-white/70 text-base sm:text-xl font-medium italic leading-relaxed">&quot;{result.message}&quot;</p>
                  
                  {result.simulation && (
                    <div className="pt-4 flex justify-center sm:justify-start">
                      <button 
                        onClick={() => setShowIntel(true)}
                        className="flex items-center gap-2 px-4 py-2 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 text-[10px] font-black tracking-widest"
                      >
                        <Activity className="w-3.5 h-3.5" /> VER SIMULAÇÃO REAL-TIME
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Security Grid - Mobile 2x2, Desktop 4x1 */}
            {result.security_audit && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
                <MetricCard label="Honeypot" active={result.security_audit.is_honeypot} danger />
                <MetricCard label="Blacklist" active={result.security_audit.is_blacklisted} danger />
                <MetricCard label="Ownership" active={result.security_audit.can_take_back_ownership} warning icon={<Lock className="w-4 h-4" />} />
                <MetricCard label="In-DEX" active={result.security_audit.is_in_dex} success icon={<ShieldCheck className="w-4 h-4" />} />
              </div>
            )}

            {/* Discovery Path */}
            {result.type === 'discovery' && (
              <div className="p-6 sm:p-10 rounded-[32px] sm:rounded-[40px] border border-white/10 bg-white/[0.02] backdrop-blur-3xl space-y-8">
                <h2 className="text-2xl sm:text-3xl font-black tracking-tighter flex items-center gap-3">
                  <Globe className="text-cyan-400" /> Smart Route: {query.split(' ')[0].toUpperCase()}
                </h2>
                <div className="space-y-6 pl-6 border-l border-white/5">
                  {result.data?.steps?.map((step: string, i: number) => (
                    <div key={i} className="relative">
                      <div className="absolute -left-[31px] top-1 w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_8px_#22d3ee]" />
                      <p className="text-white/80 text-sm sm:text-base font-semibold">{step}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Footer Minimalist */}
      <footer className="mt-20 sm:mt-32 pb-12 opacity-30 flex flex-col items-center gap-4">
        <p className="text-[9px] font-black tracking-[0.4em] uppercase text-center px-8">
          Powered by vibe-to-code Protocol • Military Grade Security
        </p>
        <div className="h-px w-12 bg-white/20" />
      </footer>
    </div>
  );
}
