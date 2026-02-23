"use client";

import React, { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from 'next/image';
import { 
  ShieldCheck, ShieldAlert, Search, Cpu, 
  Globe, Zap, Info, ExternalLink, X, TrendingUp, BarChart3, 
  Lock, Unlock, AlertTriangle, Fingerprint, Activity, MousePointer2, 
  ChevronUp, Send, User, Bot, Sparkles, MessageSquare
} from 'lucide-react';

// --- Types ---
type MessageRole = 'user' | 'assistant';
type MessageType = 'text' | 'risk' | 'discovery' | 'audit';

interface Message {
  id: string;
  role: MessageRole;
  content: string;
  type?: MessageType;
  data?: any;
  timestamp: Date;
}

// --- Components ---

const TrustGauge = React.memo(({ score }: { score: number }) => {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = useMemo(() => circumference - (score / 100) * circumference, [score, circumference]);
  const color = useMemo(() => score > 70 ? '#22c55e' : score > 40 ? '#eab308' : '#ef4444', [score]);

  return (
    <div className="relative flex items-center justify-center w-24 h-24 sm:w-28 sm:h-28">
      <svg className="w-full h-full transform -rotate-90">
        <circle cx="50%" cy="50%" r={radius} stroke="currentColor" strokeWidth="6" fill="transparent" className="text-white/5" />
        <motion.circle 
          cx="50%" cy="50%" r={radius} stroke={color} strokeWidth="6" fill="transparent" 
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-xl sm:text-2xl font-black">{score}</span>
        <span className="text-[6px] sm:text-[7px] font-bold text-white/30 tracking-[0.2em]">SCORE</span>
      </div>
    </div>
  );
});

const MetricCard = React.memo(({ label, active, danger, warning, success, icon }: any) => (
  <div className={`p-3 rounded-xl border backdrop-blur-xl flex flex-col items-center gap-2 transition-all ${
    active ? (danger ? 'bg-red-500/10 border-red-500/30 text-red-400' : warning ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400' : 'bg-green-500/10 border-green-500/30 text-green-400') 
    : 'bg-white/5 border-white/10 text-white/10'
  }`}>
    {icon || (active ? <AlertTriangle className="w-3 h-3" /> : <ShieldCheck className="w-3 h-3" />)}
    <span className="text-[8px] font-black uppercase tracking-widest">{label}</span>
  </div>
));

// --- Main Page ---

export default function SafeSentinelChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: "Olá, eu sou a **MarIA**. Sou sua especialista em segurança Web3 e estratégia da Oratech. Como posso proteger seus ativos hoje?",
      timestamp: new Date(),
    }
  ]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async () => {
    if (!query.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const apiUrl = '/api-engine';
      
      // 1. Extract Intent
      const intentResponse = await fetch(`${apiUrl}/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userMessage.content })
      });
      const intent = await intentResponse.json();

      // 2. Decide Action (Sentinel vs Discovery)
      // For now, let's assume if it looks like a transfer, it's Sentinel
      if (intent.asset || intent.address) {
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
        
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.message,
          type: 'risk',
          data: data,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Fallback or Discovery
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: "Entendi. Você gostaria de descobrir a melhor rota para algum ativo ou prefere que eu analise uma transação específica?",
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        id: 'error',
        role: 'assistant',
        content: "Desculpe, estou tendo problemas para me conectar ao motor SafeSentinel. Verifique sua conexão.",
        timestamp: new Date(),
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-[#020202] text-white relative">
      {/* Background Mesh */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] bg-cyan-500/5 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-5%] right-[-5%] w-[400px] h-[400px] bg-purple-500/5 blur-[120px] rounded-full" />
      </div>

      {/* Header */}
      <header className="glass-dark z-20 px-6 py-4 flex items-center justify-between sticky top-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-cyan-500 to-purple-600 flex items-center justify-center p-[1px]">
            <div className="w-full h-full rounded-full bg-[#020202] flex items-center justify-center">
              <Bot className="w-5 h-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <h1 className="font-black tracking-tight text-sm">SafeSentinel</h1>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
              <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest">MarIA Online</span>
            </div>
          </div>
        </div>
        <div className="hidden sm:flex items-center gap-4">
           <div className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[9px] font-black tracking-widest text-white/40">
             V2.0 ALPHA
           </div>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-grow overflow-y-auto px-4 sm:px-6 py-8 custom-scrollbar relative z-10 flex flex-col gap-8">
        <div className="max-w-3xl mx-auto w-full flex flex-col gap-10">
          {messages.map((msg) => (
            <motion.div 
              key={msg.id}
              initial={{ opacity: 0, y: 10, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} gap-3`}
            >
              {/* Message Header */}
              <div className="flex items-center gap-2 px-2">
                {msg.role === 'assistant' ? (
                  <>
                    <Sparkles className="w-3 h-3 text-cyan-400" />
                    <span className="text-[10px] font-black uppercase tracking-widest text-white/30">MarIA Intelligence</span>
                  </>
                ) : (
                  <span className="text-[10px] font-black uppercase tracking-widest text-white/30">Você</span>
                )}
              </div>

              {/* Bubble */}
              <div className={`max-w-[85%] sm:max-w-[80%] p-4 sm:p-5 rounded-[24px] sm:rounded-[32px] transition-all ${
                msg.role === 'user' 
                ? 'bg-white text-black font-semibold' 
                : 'glass shadow-2xl'
              }`}>
                <p className="text-sm sm:text-base leading-relaxed whitespace-pre-wrap">
                  {msg.content}
                </p>

                {/* Rich Data rendering */}
                {msg.type === 'risk' && msg.data && (
                  <div className="mt-6 space-y-6">
                    <div className={`p-5 rounded-[20px] sm:rounded-[28px] border overflow-hidden relative ${
                      msg.data.risk_level === 'LOW' ? 'bg-green-500/5 border-green-500/20' : 
                      msg.data.risk_level === 'MEDIUM' ? 'bg-yellow-500/5 border-yellow-500/20' : 
                      'bg-red-500/5 border-red-500/20'
                    }`}>
                      <div className="flex flex-col sm:flex-row items-center gap-6">
                        <TrustGauge score={msg.data.trust_score} />
                        <div className="text-center sm:text-left">
                          <h4 className="text-xl font-black tracking-tight mb-1">{msg.data.title}</h4>
                          <p className="text-xs text-white/60 font-medium">Análise de risco probabilística</p>
                        </div>
                      </div>
                    </div>

                    {msg.data.security_audit && (
                      <div className="grid grid-cols-2 gap-2">
                        <MetricCard label="Honeypot" active={msg.data.security_audit.is_honeypot} danger />
                        <MetricCard label="Blacklist" active={msg.data.security_audit.is_blacklisted} danger />
                        <MetricCard label="Ownership" active={msg.data.security_audit.can_take_back_ownership} warning icon={<Lock className="w-3 h-3" />} />
                        <MetricCard label="In-DEX" active={msg.data.security_audit.is_in_dex} success icon={<ShieldCheck className="w-3 h-3" />} />
                      </div>
                    )}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
          
          {loading && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-3 text-white/30"
            >
              <Activity className="w-4 h-4 animate-spin" />
              <span className="text-xs font-black uppercase tracking-[0.2em]">MarIA está pensando...</span>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <div className="glass-dark z-30 p-4 sm:p-6 sticky bottom-0">
        <div className="max-w-3xl mx-auto relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-[24px] sm:rounded-[32px] blur-md opacity-40 group-focus-within:opacity-100 transition-all duration-500" />
          <div className="relative bg-[#0A0A0A] border border-white/10 rounded-[20px] sm:rounded-[28px] flex items-center p-1.5 gap-2 shadow-2xl">
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Diga para onde quer enviar ou peça uma análise..."
              className="flex-grow bg-transparent border-none px-4 py-3 sm:py-4 text-sm sm:text-base focus:outline-none placeholder:text-white/10 font-medium"
              style={{ fontSize: '16px' }}
            />
            <button 
              onClick={handleSend}
              disabled={!query.trim() || loading}
              className="w-10 h-10 sm:w-12 sm:h-12 flex items-center justify-center bg-white text-black rounded-full active:scale-95 transition-all disabled:opacity-20 shadow-xl"
            >
              <Send className="w-4 h-4 sm:w-5 sm:h-5" />
            </button>
          </div>
        </div>
        <p className="text-[8px] text-center mt-4 text-white/20 font-black uppercase tracking-[0.2em]">
          SafeSentinel Alpha • Oratech Intelligent Security
        </p>
      </div>
    </div>
  );
}
