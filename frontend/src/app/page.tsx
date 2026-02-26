"use client";

import React, { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldCheck, ShieldAlert, Search, Cpu, 
  Globe, Zap, Info, ExternalLink, X, TrendingUp, BarChart3, 
  Lock, Unlock, AlertTriangle, Fingerprint, Activity, MousePointer2, 
  ChevronUp, Send, User, Bot, Sparkles, MessageSquare,
  Terminal as TerminalIcon, CpuIcon, Binary, Share2, Github
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { RainbowButton } from '@/components/ui/rainbow-button';
import Particles from '@/components/ui/particles';

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
  const color = useMemo(() => score > 70 ? '#00F2FF' : score > 40 ? '#eab308' : '#ef4444', [score]);

  return (
    <div className="relative flex items-center justify-center w-24 h-24 sm:w-28 sm:h-28">
      <svg className="w-full h-full transform -rotate-90">
        <circle cx="50%" cy="50%" r={radius} stroke="currentColor" strokeWidth="4" fill="transparent" className="text-white/5" />
        <motion.circle 
          cx="50%" cy="50%" r={radius} stroke={color} strokeWidth="4" fill="transparent" 
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-xl sm:text-2xl font-black text-glow">{score}</span>
        <span className="text-[6px] sm:text-[7px] font-bold text-white/30 tracking-[0.2em]">TRUST</span>
      </div>
    </div>
  );
});

TrustGauge.displayName = 'TrustGauge';

export default function SafeSentinelApp() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'SISTEMA_ATIVO: Olá, sou a MarIA. Cole o endereço de destino ou descreva sua intenção de transferência para análise on-chain.',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll logic
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = useCallback(async () => {
    if (!input.trim() || isProcessing) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsProcessing(true);

    // Simulate AI response logic
    setTimeout(() => {
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'ANÁLISE_CONCLUÍDA: O endereço fornecido foi validado. Não foram encontrados registros em blacklists conhecidas. Score de confiança: 98%.',
        type: 'risk',
        data: { score: 98 },
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMsg]);
      setIsProcessing(false);
    }, 1500);
  }, [input, isProcessing]);

  return (
    <main className="relative min-h-screen w-full bg-background font-sans overflow-hidden selection:bg-primary/30">
      {/* Background Layer */}
      <Particles className="opacity-40" />
      <div className="fixed inset-0 cyber-grid pointer-events-none" />
      <div className="fixed inset-0 bg-gradient-to-b from-transparent via-transparent to-background/80 pointer-events-none" />
      
      {/* Scanline Effect */}
      <div className="scanline" />

      {/* Header */}
      <nav className="relative z-50 flex items-center justify-between px-6 py-4 border-b border-white/5 bg-background/40 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="relative">
            <ShieldCheck className="w-8 h-8 text-primary animate-pulse" />
            <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-black tracking-tighter text-white leading-none">SAFE<span className="text-primary">SENTINEL</span></span>
            <span className="text-[8px] font-bold text-white/40 tracking-[0.3em] uppercase">v2.0 Protocol</span>
          </div>
        </div>
        
        <div className="hidden md:flex items-center gap-6">
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
            <span className="text-[10px] font-mono text-white/60 tracking-wider">NETWORK: MAINNET</span>
          </div>
          <button className="text-white/40 hover:text-white transition-colors">
            <Github className="w-5 h-5" />
          </button>
        </div>
      </nav>

      {/* Main Content Interface */}
      <div className="relative z-10 max-w-5xl mx-auto h-[calc(100vh-73px)] flex flex-col md:p-6 lg:p-10">
        
        {/* Chat / Analysis Area */}
        <div className="flex-1 flex flex-col glass-morphism rounded-none md:rounded-3xl overflow-hidden border-x-0 md:border-x">
          
          {/* Messages Display */}
          <div 
            ref={scrollRef}
            className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 custom-scrollbar"
          >
            <AnimatePresence initial={false}>
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  className={cn(
                    "flex flex-col gap-2 max-w-[90%] md:max-w-[80%]",
                    msg.role === 'user' ? "ml-auto items-end" : "items-start"
                  )}
                >
                  <div className="flex items-center gap-2 mb-1">
                    {msg.role === 'assistant' ? (
                      <>
                        <div className="p-1 rounded bg-primary/10 border border-primary/20">
                          <Bot className="w-3 h-3 text-primary" />
                        </div>
                        <span className="text-[9px] font-bold text-primary tracking-[0.2em] uppercase">MarIA_CORE</span>
                      </>
                    ) : (
                      <>
                        <span className="text-[9px] font-bold text-white/40 tracking-[0.2em] uppercase">OPERATOR</span>
                        <div className="p-1 rounded bg-white/5 border border-white/10">
                          <User className="w-3 h-3 text-white/60" />
                        </div>
                      </>
                    )}
                  </div>

                  <div className={cn(
                    "px-5 py-4 rounded-2xl text-sm md:text-base leading-relaxed",
                    msg.role === 'user' 
                      ? "bg-primary/10 text-primary border border-primary/20 rounded-tr-none" 
                      : "bg-white/5 text-white/90 border border-white/10 rounded-tl-none"
                  )}>
                    {msg.content}
                  </div>

                  {msg.type === 'risk' && msg.data && (
                    <motion.div 
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="mt-2 w-full glass-morphism rounded-2xl p-6 flex flex-col md:flex-row items-center gap-6 border-primary/30"
                    >
                      <TrustGauge score={msg.data.score} />
                      <div className="flex-1 space-y-2 text-center md:text-left">
                        <div className="text-sm font-bold text-primary flex items-center justify-center md:justify-start gap-2">
                          <ShieldCheck className="w-4 h-4" />
                          ENDEREÇO VERIFICADO
                        </div>
                        <p className="text-xs text-white/60">
                          Esta transação parece segura. O destino é uma EOA validada e não possui histórico de atividades suspeitas.
                        </p>
                        <div className="flex flex-wrap gap-2 pt-2 justify-center md:justify-start">
                          <span className="text-[9px] px-2 py-1 rounded bg-white/5 border border-white/10 text-white/40 font-mono">NON_CONTRACT: TRUE</span>
                          <span className="text-[9px] px-2 py-1 rounded bg-white/5 border border-white/10 text-white/40 font-mono">HISTORY: CLEAN</span>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
            
            {isProcessing && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center gap-3 text-primary/60 animate-pulse"
              >
                <div className="flex gap-1">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.3s]" />
                  <div className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.15s]" />
                  <div className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" />
                </div>
                <span className="text-[10px] font-mono tracking-widest uppercase">Processando Heurística...</span>
              </motion.div>
            )}
          </div>

          {/* Input Area */}
          <div className="p-4 md:p-8 bg-black/40 border-t border-white/5">
            <div className="relative group max-w-4xl mx-auto">
              <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 to-blue-500/20 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000" />
              <div className="relative flex flex-col md:flex-row items-center gap-4 bg-[#050505] border border-white/10 rounded-2xl p-2 md:pl-6 pr-2">
                <div className="hidden md:block">
                  <TerminalIcon className="w-5 h-5 text-primary/40" />
                </div>
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  placeholder="Explique o que deseja fazer ou cole um hash..."
                  className="flex-1 w-full bg-transparent border-none outline-none text-white placeholder:text-white/20 py-4 text-sm md:text-base resize-none min-h-[60px]"
                  rows={1}
                />
                <RainbowButton 
                  onClick={handleSend}
                  disabled={!input.trim() || isProcessing}
                  className="w-full md:w-auto h-12 md:h-11"
                >
                  <Sparkles className="w-4 h-4 mr-2" />
                  ANALISAR
                </RainbowButton>
              </div>
            </div>
            
            {/* Status Footer */}
            <div className="mt-6 flex flex-wrap items-center justify-center gap-x-8 gap-y-2 opacity-30 grayscale hover:opacity-100 hover:grayscale-0 transition-all duration-500">
              <div className="flex items-center gap-2">
                <CpuIcon className="w-3 h-3" />
                <span className="text-[9px] font-bold tracking-[0.2em] uppercase">Gemini 2.0 Flash</span>
              </div>
              <div className="flex items-center gap-2">
                <Binary className="w-3 h-3" />
                <span className="text-[9px] font-bold tracking-[0.2em] uppercase">On-Chain Forensics</span>
              </div>
              <div className="flex items-center gap-2">
                <Share2 className="w-3 h-3" />
                <span className="text-[9px] font-bold tracking-[0.2em] uppercase">vibe-to-code</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx global>{`
        .text-glow {
          text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
        }
        
        .cyber-grid {
          background-image: linear-gradient(to right, rgba(0, 242, 255, 0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(0, 242, 255, 0.03) 1px, transparent 1px);
          background-size: 50px 50px;
        }

        @keyframes rainbow {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        .animate-rainbow {
          animation: rainbow 3s linear infinite;
        }

        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(0, 242, 255, 0.1);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(0, 242, 255, 0.2);
        }
      `}</style>
    </main>
  );
}
