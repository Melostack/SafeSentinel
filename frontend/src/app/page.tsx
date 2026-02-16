"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldCheck, ShieldAlert, Search, Cpu, 
  Globe, Zap, Info, ExternalLink, X, TrendingUp, BarChart3, 
  Lock, Unlock, AlertTriangle, Fingerprint, Activity, MousePointer2
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
  };

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val);
  };

  const TrustGauge = ({ score }: { score: number }) => {
    const radius = 45;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;
    const color = score > 70 ? '#22c55e' : score > 40 ? '#eab308' : '#ef4444';

    return (
      <div className="relative flex items-center justify-center w-32 h-32">
        <svg className="w-full h-full transform -rotate-90">
          <circle cx="64" cy="64" r={radius} stroke="currentColor" strokeWidth="8" fill="transparent" className="text-white/5" />
          <motion.circle 
            cx="64" cy="64" r={radius} stroke={color} strokeWidth="8" fill="transparent" 
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute flex flex-col items-center">
          <span className="text-3xl font-black">{score}</span>
          <span className="text-[8px] font-bold text-white/30 tracking-[0.2em]">SCORE</span>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#020202] text-white selection:bg-cyan-500/30 font-sans flex flex-col items-center p-4 sm:p-12 overflow-x-hidden relative">
      {/* Premium Mesh Gradient Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-cyan-500/10 blur-[140px] rounded-full animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-purple-500/10 blur-[140px] rounded-full animate-pulse" />
        <div className="absolute top-[30%] left-[40%] w-[300px] h-[300px] bg-blue-500/5 blur-[100px] rounded-full" />
      </div>

      {/* Main Container */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-4xl z-10 flex flex-col items-center"
      >
        {/* Header Branding */}
        <header className="flex flex-col items-center mb-16">
          <motion.div 
            whileHover={{ scale: 1.05 }}
            className="px-5 py-2 rounded-full border border-white/10 bg-white/5 backdrop-blur-2xl flex items-center gap-3 mb-8 shadow-inner"
          >
            <div className="relative">
              <Zap className="w-4 h-4 text-cyan-400 fill-cyan-400" />
              <div className="absolute inset-0 bg-cyan-400 blur-md opacity-50" />
            </div>
            <span className="text-[10px] font-black tracking-[0.3em] uppercase text-white/80">Melostack Sentinel v2.0</span>
          </motion.div>
          <h1 className="text-6xl sm:text-7xl font-black tracking-tighter mb-4 text-center bg-gradient-to-b from-white via-white to-white/20 bg-clip-text text-transparent">
            SafeSentinel
          </h1>
          <div className="flex items-center gap-2 text-white/40 font-bold uppercase tracking-[0.2em] text-[10px] sm:text-xs">
            <Fingerprint className="w-3 h-3" />
            The Web3 Interpretive Security Layer
          </div>
        </header>

        {/* Command Center */}
        <div className="w-full relative group mb-12">
          <div className="absolute -inset-1.5 bg-gradient-to-r from-cyan-500/30 via-blue-500/30 to-purple-500/30 rounded-[32px] blur-xl opacity-20 group-focus-within:opacity-60 transition-all duration-700" />
          <div className="relative bg-[#0A0A0A]/60 border border-white/10 rounded-[28px] p-2.5 flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shadow-[0_20px_50px_rgba(0,0,0,0.5)] backdrop-blur-3xl">
            <div className="hidden sm:flex pl-5">
              <Search className="w-6 h-6 text-white/20" />
            </div>
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={mode === 'sentinel' ? "Ex: Mandar USDT da Binance..." : "Ex: OKB X-Layer"}
              className="flex-grow bg-transparent border-none px-5 py-5 sm:py-5 text-lg sm:text-xl focus:outline-none placeholder:text-white/5 font-semibold selection:bg-cyan-500/50"
              onKeyDown={(e) => e.key === 'Enter' && handleProcess()}
            />
            <button 
              onClick={handleProcess}
              disabled={loading || query.length < 2}
              className="bg-white text-black px-10 py-5 sm:py-4 rounded-[22px] font-black text-sm hover:bg-cyan-50 active:scale-95 transition-all disabled:opacity-20 shadow-xl"
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 animate-spin" />
                  ANALISANDO
                </div>
              ) : "EXECUTAR"}
            </button>
          </div>
        </div>

        {/* Mode Selector */}
        <div className="flex p-1.5 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl mb-12">
          {['sentinel', 'discovery'].map((m) => (
            <button 
              key={m}
              onClick={() => { setMode(m as any); setResult(null); }}
              className={`px-8 py-2.5 rounded-xl text-[10px] font-black transition-all tracking-[0.1em] ${mode === m ? 'bg-white text-black shadow-lg' : 'text-white/40 hover:text-white'}`}
            >
              {m.toUpperCase()}
            </button>
          ))}
        </div>

        {/* Dynamic Results Section */}
        <AnimatePresence mode='wait'>
          {result && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.98, y: 30 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98, y: -30 }}
              className="w-full space-y-8"
            >
              {/* Main Risk Card */}
              <div className={`p-8 sm:p-12 rounded-[40px] border relative overflow-hidden backdrop-blur-3xl shadow-2xl ${
                result.risk_level === 'LOW' ? 'bg-green-500/[0.03] border-green-500/20' : 
                result.risk_level === 'MEDIUM' ? 'bg-yellow-500/[0.03] border-yellow-500/20' : 
                'bg-red-500/[0.03] border-red-500/20'
              }`}>
                <div className="flex flex-col md:flex-row items-center sm:items-start gap-8 sm:gap-12 relative z-10">
                  <div className="shrink-0 flex flex-col items-center gap-6">
                    <TrustGauge score={result.trust_score} />
                    <div className={`px-4 py-1.5 rounded-full text-[10px] font-black tracking-widest ${
                      result.risk_level === 'LOW' ? 'bg-green-500/20 text-green-400 border border-green-500/30' : 
                      result.risk_level === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' : 
                      'bg-red-500/20 text-red-400 border border-red-500/30'
                    }`}>
                      RISCO {result.risk_level}
                    </div>
                  </div>

                  <div className="flex-grow space-y-6">
                    <header className="flex flex-col gap-2">
                      <h2 className="text-3xl sm:text-4xl font-black tracking-tighter leading-tight">{result.title}</h2>
                      <p className="text-white/30 font-bold uppercase tracking-[0.2em] text-[10px]">Veredito do Protocolo SafeTransfer</p>
                    </header>
                    
                    <p className="text-white/80 text-lg sm:text-xl leading-relaxed font-medium italic serif">
                      &quot;{result.message}&quot;
                    </p>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-6">
                      <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/5">
                        <Cpu className="w-5 h-5 text-cyan-400" />
                        <div>
                          <span className="block text-[8px] font-black text-white/30 uppercase tracking-widest">Network Forensic</span>
                          <span className="text-xs font-bold">{result.on_chain?.type}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/5">
                        <ShieldCheck className="w-5 h-5 text-purple-400" />
                        <div>
                          <span className="block text-[8px] font-black text-white/30 uppercase tracking-widest">Target Status</span>
                          <span className="text-xs font-bold">Verified on {parsedIntent?.network || 'Blockchain'}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Security Audit Grid (GoPlus) */}
              {result.security_audit && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <SecurityMetric label="Honeypot" active={result.security_audit.is_honeypot} danger />
                  <SecurityMetric label="Blacklist" active={result.security_audit.is_blacklisted} danger />
                  <SecurityMetric label="Owner" active={result.security_audit.can_take_back_ownership} warning icon={<Lock className="w-4 h-4" />} />
                  <SecurityMetric label="Verified" active={result.security_audit.is_in_dex} success icon={<ShieldCheck className="w-4 h-4" />} />
                </div>
              )}

              {/* Discovery Timeline */}
              {result.type === 'discovery' && (
                <div className="p-8 sm:p-12 rounded-[40px] border border-white/10 bg-[#0A0A0A]/40 backdrop-blur-3xl space-y-10">
                  <header className="flex items-center justify-between">
                    <h2 className="text-3xl font-black tracking-tighter flex items-center gap-4">
                      <Globe className="w-8 h-8 text-cyan-400" />
                      Smart Route: {query.split(' ')[0].toUpperCase()}
                    </h2>
                    <div className="px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-[10px] font-black text-cyan-400 tracking-widest uppercase">
                      Best Path Identified
                    </div>
                  </header>

                  <div className="relative space-y-8 pl-8 border-l border-white/5">
                    {result.data.steps?.map((step: string, i: number) => (
                      <motion.div 
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        key={i} 
                        className="relative"
                      >
                        <div className="absolute left-[-41px] top-0 w-5 h-5 rounded-full bg-[#020202] border-2 border-white/20 flex items-center justify-center">
                          <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-[0_0_10px_#22d3ee]" />
                        </div>
                        <p className="text-white/80 text-lg font-semibold">{step}</p>
                      </motion.div>
                    ))}
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-10 border-t border-white/5">
                    <DetailItem label="Primary Source" value={result.data.cex_source} />
                    <DetailItem label="Bridge Engine" value={result.data.recommended_bridge || 'Native'} />
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        <footer className="mt-32 pb-12 flex flex-col items-center gap-8 opacity-20 hover:opacity-100 transition-all duration-1000">
          <div className="flex gap-12">
            <FooterIcon icon={<Globe />} label="Global Liquidity" />
            <FooterIcon icon={<ShieldCheck />} label="Military Grade Security" />
            <FooterIcon icon={<MousePointer2 />} label="One-Click Audit" />
          </div>
          <div className="flex flex-col items-center gap-2">
            <p className="text-[10px] font-black text-white/40 uppercase tracking-[0.5em]">
              Powered by Oratech Vibe-to-Code Protocol
            </p>
            <div className="h-px w-12 bg-gradient-to-r from-transparent via-white/20 to-transparent" />
          </div>
        </footer>
      </motion.div>
    </div>
  );
}

// Sub-components for cleaner structure
const SecurityMetric = ({ label, active, danger, warning, success, icon }: any) => (
  <div className={`p-4 rounded-2xl border backdrop-blur-xl flex flex-col items-center gap-3 transition-all ${
    active ? (danger ? 'bg-red-500/10 border-red-500/30 text-red-400' : warning ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400' : 'bg-green-500/10 border-green-500/30 text-green-400') 
    : 'bg-white/5 border-white/10 text-white/20'
  }`}>
    {icon || (active ? <AlertTriangle className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4" />)}
    <span className="text-[10px] font-black uppercase tracking-widest">{label}</span>
  </div>
);

const DetailItem = ({ label, value }: any) => (
  <div className="p-6 rounded-3xl bg-white/5 border border-white/10 hover:bg-white/[0.07] transition-colors group">
    <span className="block text-[10px] font-black text-white/30 uppercase tracking-[0.2em] mb-2 group-hover:text-cyan-400 transition-colors">{label}</span>
    <span className="text-xl font-bold tracking-tight">{value}</span>
  </div>
);

const FooterIcon = ({ icon, label }: any) => (
  <div className="flex flex-col items-center gap-3 group cursor-default">
    <div className="p-3 rounded-xl bg-white/5 group-hover:bg-cyan-500/20 group-hover:text-cyan-400 transition-all border border-transparent group-hover:border-cyan-500/20">
      {React.cloneElement(icon as React.ReactElement, { className: "w-5 h-5" })}
    </div>
    <span className="text-[8px] font-black uppercase tracking-[0.2em]">{label}</span>
  </div>
);
