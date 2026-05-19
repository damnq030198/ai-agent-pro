'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Send, User, Bot, Sparkles, Loader2, Copy, Check, Terminal, ExternalLink, Code2, Play, ChevronRight, X, Layers, Undo2, History } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  role: 'user' | 'ai';
  content: string;
  status?: string;
}

interface Artifact {
  id: string;
  title: string;
  language: string;
  content: string;
}

export default function ChatInterface() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [activeArtifact, setActiveArtifact] = useState<Artifact | null>(null);
  const [currentStatus, setCurrentStatus] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStatus, scrollToBottom]);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleUndo = async () => {
    if (isLoading) return;
    setIsLoading(true);
    setCurrentStatus('Undoing last action...');
    
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3003/api/v1';
      const response = await fetch(`${apiUrl}/agent/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: "Undo my last file change", model_id: 'gemini-1.5-pro' })
      });
      const data = await response.json();
      
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: `🔄 **Undo Successful**: ${data.metadata.response || 'Action reverted.'}` 
      }]);
    } catch (error) {
      console.error('Undo error:', error);
    } finally {
      setIsLoading(false);
      setCurrentStatus(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    const userQuery = query;
    setMessages((prev) => [...prev, { role: 'user', content: userQuery }]);
    setQuery('');
    setIsLoading(true);
    setCurrentStatus('Warming up engines...');

    setMessages((prev) => [...prev, { role: 'ai', content: '' }]);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3003/api/v1';
      
      const response = await fetch(`${apiUrl}/agent/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery, model_id: 'gemini-1.5-pro' })
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullAIContent = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.replace('data: ', '');
              if (dataStr === '[DONE]') break;
              
              try {
                const parsed = JSON.parse(dataStr);
                const text = parsed.text || '';

                if (text.startsWith('__TOOL_CALL__:')) {
                  const toolInfo = JSON.parse(text.replace('__TOOL_CALL__:', ''));
                  setCurrentStatus(`Agent using: ${toolInfo.name}`);
                  continue;
                }
                if (text.startsWith('__TOOL_RESULT__:')) {
                  const toolResult = JSON.parse(text.replace('__TOOL_RESULT__:', ''));
                  setCurrentStatus(`Action completed: ${toolResult.name}`);
                  setTimeout(() => setCurrentStatus(null), 2000);
                  continue;
                }

                if (text) {
                  fullAIContent += text;
                  setMessages((prev) => {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = { 
                      role: 'ai', 
                      content: fullAIContent 
                    };
                    return newMessages;
                  });

                  // Artifact extraction logic
                  const codeBlockMatch = fullAIContent.match(/```(\w+)\n([\s\S]*?)```/);
                  if (codeBlockMatch) {
                    setActiveArtifact({
                      id: 'last-code',
                      title: 'Current Artifact',
                      language: codeBlockMatch[1],
                      content: codeBlockMatch[2].trim()
                    });
                  }
                }
              } catch (e) {}
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
      setCurrentStatus(null);
    }
  };

  return (
    <div className="flex h-full w-full bg-[#050506] overflow-hidden font-sans text-zinc-200">
      {/* Sidebar - Quick Actions */}
      <div className="w-16 flex flex-col items-center py-6 border-r border-white/5 bg-[#09090b]">
        <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center mb-8 shadow-lg shadow-blue-600/20">
          <Sparkles size={20} className="text-white" />
        </div>
        <div className="flex flex-col gap-6">
          <button className="p-3 text-zinc-500 hover:text-white transition-colors"><History size={20} /></button>
          <button onClick={handleUndo} className="p-3 text-zinc-500 hover:text-orange-400 transition-colors" title="Undo Last Action">
            <Undo2 size={20} />
          </button>
        </div>
        <div className="mt-auto">
          <div className="w-8 h-8 rounded-full bg-zinc-800 border border-white/10 flex items-center justify-center">
            <User size={14} />
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className={`flex flex-col h-full transition-all duration-500 ${activeArtifact ? 'w-[40%] border-r border-white/5' : 'flex-1 max-w-4xl mx-auto w-full'}`}>
        <div className="flex items-center justify-between px-8 py-6 border-b border-white/5 bg-[#09090b]/50 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <h1 className="text-sm font-black uppercase tracking-[0.3em] text-white">Orchestrator <span className="text-blue-500">v2</span></h1>
            <div className="flex items-center gap-1.5 px-2 py-0.5 bg-green-500/10 border border-green-500/20 rounded-full">
              <div className="w-1 h-1 rounded-full bg-green-500 animate-pulse"></div>
              <span className="text-[8px] font-bold text-green-500 uppercase">Live</span>
            </div>
          </div>
          {activeArtifact && (
            <button onClick={() => setActiveArtifact(null)} className="text-zinc-500 hover:text-white transition-colors">
              <ChevronRight size={20} />
            </button>
          )}
        </div>

        <div className="flex-1 overflow-y-auto px-8 py-10 space-y-10 scrollbar-hide">
          <AnimatePresence mode="popLayout">
            {messages.map((msg, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex gap-5 max-w-[95%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                  <div className={`mt-1 flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
                    msg.role === 'user' ? 'bg-blue-600 shadow-lg shadow-blue-600/20' : 'bg-zinc-800 border border-white/5'
                  }`}>
                    {msg.role === 'user' ? <User size={14} /> : <Bot size={14} className="text-blue-400" />}
                  </div>
                  <div className={`space-y-2 ${msg.role === 'user' ? 'text-right' : ''}`}>
                    <div className={`inline-block text-left p-5 rounded-2xl ${
                      msg.role === 'user' ? 'bg-[#18181b] border border-white/5' : ''
                    }`}>
                      <div className="prose prose-invert prose-sm max-w-none">
                        <ReactMarkdown 
                          remarkPlugins={[remarkGfm]}
                          components={{
                            code({ node, inline, className, children, ...props }: any) {
                              const match = /language-(\w+)/.exec(className || '');
                              return !inline && match ? (
                                <div className="my-4 rounded-xl overflow-hidden border border-white/5 bg-black/40">
                                  <div className="px-4 py-2 bg-white/5 flex justify-between items-center">
                                    <span className="text-[9px] font-black uppercase text-zinc-500 tracking-widest">{match[1]}</span>
                                    <button onClick={() => handleCopy(String(children), 'msg-code')} className="text-zinc-600 hover:text-zinc-400"><Copy size={12}/></button>
                                  </div>
                                  <SyntaxHighlighter
                                    style={vscDarkPlus}
                                    language={match[1]}
                                    PreTag="div"
                                    customStyle={{ background: 'transparent', padding: '1rem', fontSize: '12px' }}
                                  >
                                    {String(children).replace(/\n$/, '')}
                                  </SyntaxHighlighter>
                                </div>
                              ) : (
                                <code className="bg-blue-500/10 text-blue-400 px-1.5 py-0.5 rounded font-mono" {...props}>{children}</code>
                              )
                            }
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          {currentStatus && (
            <div className="flex items-center gap-3 px-12 text-zinc-500 animate-pulse">
              <Loader2 size={12} className="animate-spin" />
              <span className="text-[10px] font-black uppercase tracking-[0.2em]">{currentStatus}</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-8">
          <form onSubmit={handleSubmit} className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-3xl blur opacity-0 group-focus-within:opacity-100 transition duration-1000"></div>
            <div className="relative flex items-center bg-[#09090b] border border-white/10 rounded-2xl p-2 pr-4 shadow-2xl">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask me to build something..."
                className="flex-1 bg-transparent border-none outline-none py-4 px-4 text-sm text-white placeholder-zinc-700"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!query.trim() || isLoading}
                className="p-3 bg-white text-black rounded-xl hover:scale-105 active:scale-95 transition-all disabled:opacity-20 disabled:scale-100"
              >
                {isLoading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Artifacts Panel */}
      <AnimatePresence>
        {activeArtifact && (
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 30, stiffness: 300 }}
            className="flex-1 bg-[#09090b] flex flex-col border-l border-white/5"
          >
            <div className="flex items-center justify-between p-5 border-b border-white/5 bg-[#0c0c0e]">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-600/10 rounded-lg"><Code2 size={18} className="text-blue-500" /></div>
                <div>
                  <h2 className="text-xs font-black uppercase tracking-widest text-white">{activeArtifact.title}</h2>
                  <span className="text-[9px] text-zinc-600 font-bold uppercase">{activeArtifact.language}</span>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <button onClick={handleUndo} className="p-2 hover:bg-orange-500/10 rounded-lg text-zinc-500 hover:text-orange-500 transition-colors" title="Undo Changes">
                  <Undo2 size={18} />
                </button>
                <div className="w-[1px] h-4 bg-white/10"></div>
                <button onClick={() => setActiveArtifact(null)} className="p-2 hover:bg-white/5 rounded-lg text-zinc-500"><X size={18} /></button>
              </div>
            </div>
            <div className="flex-1 overflow-hidden flex flex-col">
              <div className="flex px-6 border-b border-white/5">
                <button className="px-4 py-4 text-[10px] font-black uppercase tracking-widest text-blue-500 border-b-2 border-blue-500">Source</button>
                <button className="px-4 py-4 text-[10px] font-black uppercase tracking-widest text-zinc-600 hover:text-zinc-400">Preview</button>
              </div>
              <div className="flex-1 overflow-auto p-6 bg-[#050506]">
                <SyntaxHighlighter
                  style={vscDarkPlus}
                  language={activeArtifact.language}
                  showLineNumbers
                  customStyle={{ background: 'transparent', margin: 0, fontSize: '12px' }}
                >
                  {activeArtifact.content}
                </SyntaxHighlighter>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
