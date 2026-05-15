"use client";

import React, { useState, useEffect, useRef } from "react";
import { Send, Bot, User, Sparkles, Globe, Settings, Cpu, ChevronDown, BarChart3, MessageSquare, CreditCard, Activity, Clock } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";

interface Message {
  id: string;
  role: "user" | "ai";
  content: string;
  timestamp: Date;
}

interface AnalyticsData {
  total_input_tokens: number;
  total_output_tokens: number;
  estimated_cost_usd: string;
  request_count: number;
  history: any[];
}

export default function App() {
  const [activeTab, setActiveTab] = useState<"chat" | "analytics">("chat");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState("claude-3-5-sonnet");
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const models = [
    { id: "claude-3-5-sonnet", name: "Claude 3.5 Sonnet", icon: <Sparkles className="w-4 h-4 text-purple-400" /> },
    { id: "gpt-4o", name: "GPT-4o Premium", icon: <Cpu className="w-4 h-4 text-green-400" /> },
    { id: "gemini-1.5-pro", name: "Gemini 1.5 Pro", icon: <Globe className="w-4 h-4 text-blue-400" /> },
  ];

  useEffect(() => {
    if (activeTab === "analytics") {
      fetchAnalytics();
    }
  }, [activeTab]);

  const fetchAnalytics = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000/api/v1";
      const res = await axios.get(`${apiUrl}/analytics/usage`);
      setAnalytics(res.data.metadata);
    } catch (e) {
      console.error("Failed to fetch analytics", e);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const userMsg: Message = { id: Date.now().toString(), role: "user", content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post("http://localhost:3000/api/v1/agent/query", { query: input, model_id: selectedModel });
      const aiMsg: Message = { id: (Date.now() + 1).toString(), role: "ai", content: res.data.metadata.response || res.data.metadata, timestamp: new Date() };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      setMessages(prev => [...prev, { id: "err", role: "ai", content: "Error connecting to AI Server.", timestamp: new Date() }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#0a0a0c] text-white overflow-hidden">
      {/* Sidebar */}
      <aside className="w-20 lg:w-64 border-r border-white/5 flex flex-col items-center lg:items-start py-6 glass z-20">
        <div className="px-6 mb-10 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Bot className="w-6 h-6" />
          </div>
          <h1 className="hidden lg:block font-bold text-xl tracking-tight">AI Pro</h1>
        </div>

        <nav className="flex-1 w-full px-3 space-y-2">
          <button 
            onClick={() => setActiveTab("chat")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === "chat" ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20" : "text-zinc-500 hover:bg-white/5 hover:text-white"}`}
          >
            <MessageSquare className="w-5 h-5" />
            <span className="hidden lg:block font-medium">Chat Agent</span>
          </button>
          <button 
            onClick={() => setActiveTab("analytics")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === "analytics" ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20" : "text-zinc-500 hover:bg-white/5 hover:text-white"}`}
          >
            <BarChart3 className="w-5 h-5" />
            <span className="hidden lg:block font-medium">Analytics</span>
          </button>
        </nav>

        <div className="px-3 w-full mt-auto">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-zinc-500 hover:bg-white/5 hover:text-white transition-all">
            <Settings className="w-5 h-5" />
            <span className="hidden lg:block font-medium">Settings</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative overflow-hidden">
        {activeTab === "chat" ? (
          <>
            <header className="px-8 py-4 border-b border-white/5 flex justify-between items-center glass">
              <div className="flex items-center gap-4">
                <div className="relative group">
                  <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all">
                    {models.find(m => m.id === selectedModel)?.icon}
                    <span className="font-medium">{models.find(m => m.id === selectedModel)?.name}</span>
                    <ChevronDown className="w-4 h-4 text-zinc-500" />
                  </button>
                  <div className="absolute left-0 top-full mt-2 w-56 py-2 glass rounded-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-30">
                    {models.map(m => (
                      <button key={m.id} onClick={() => setSelectedModel(m.id)} className="w-full flex items-center gap-3 px-4 py-2 hover:bg-white/5 text-sm transition-colors">
                        {m.icon} {m.name}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </header>

            <main className="flex-1 overflow-y-auto p-8 space-y-6">
              <div className="max-w-4xl mx-auto space-y-8">
                {messages.length === 0 && (
                  <div className="py-20 text-center space-y-4">
                    <h2 className="text-4xl font-bold text-white/90 italic">Unleash the Power of AI</h2>
                    <p className="text-zinc-500">How can I assist your workflow today?</p>
                  </div>
                )}
                {messages.map(msg => (
                  <motion.div key={msg.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                    <div className={`max-w-[85%] px-5 py-3 rounded-2xl ${msg.role === "user" ? "chat-bubble-user" : "chat-bubble-ai border border-white/5"}`}>
                      <ReactMarkdown remarkPlugins={[remarkGfm]} components={{
                        code({ node, inline, className, children, ...props }: any) {
                          const match = /language-(\w+)/.exec(className || "");
                          return !inline && match ? (
                            <SyntaxHighlighter style={atomDark} language={match[1]} PreTag="div" className="rounded-lg my-2" {...props}>
                              {String(children).replace(/\n$/, "")}
                            </SyntaxHighlighter>
                          ) : (
                            <code className="bg-black/30 px-1 rounded text-blue-300" {...props}>{children}</code>
                          );
                        }
                      }}>
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  </motion.div>
                ))}
                {isLoading && <div className="text-zinc-500 italic text-sm animate-pulse">Agent is thinking...</div>}
                <div ref={messagesEndRef} />
              </div>
            </main>

            <footer className="p-8">
              <div className="max-w-4xl mx-auto flex gap-3 p-2 glass rounded-2xl border border-white/10 focus-within:ring-2 ring-blue-500/50 transition-all">
                <input 
                  type="text" 
                  value={input} 
                  onChange={(e) => setInput(e.target.value)} 
                  onKeyDown={(e) => e.key === "Enter" && handleSend()} 
                  placeholder="Ask me anything..." 
                  className="flex-1 bg-transparent border-none focus:ring-0 px-4"
                />
                <button onClick={handleSend} disabled={isLoading || !input.trim()} className="bg-blue-600 p-3 rounded-xl hover:bg-blue-500 transition-all shadow-lg shadow-blue-500/20">
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </footer>
          </>
        ) : (
          <main className="flex-1 overflow-y-auto p-12">
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="max-w-5xl mx-auto space-y-10">
              <header>
                <h2 className="text-3xl font-bold mb-2">Usage Analytics</h2>
                <p className="text-zinc-500 text-sm">Monitor your AI consumption and estimated costs in real-time.</p>
              </header>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  { label: "Total Requests", value: analytics?.request_count || 0, icon: <Activity className="text-blue-400" /> },
                  { label: "Total Tokens", value: (analytics?.total_input_tokens || 0) + (analytics?.total_output_tokens || 0), icon: <Sparkles className="text-purple-400" /> },
                  { label: "Estimated Cost", value: `$${analytics?.estimated_cost_usd || "0.00"}`, icon: <CreditCard className="text-green-400" /> },
                ].map(stat => (
                  <div key={stat.label} className="p-6 glass rounded-2xl border border-white/5 space-y-4">
                    <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">{stat.icon}</div>
                    <div>
                      <p className="text-zinc-500 text-sm font-medium">{stat.label}</p>
                      <p className="text-2xl font-bold mt-1">{stat.value}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="glass rounded-2xl border border-white/5 overflow-hidden">
                <div className="px-6 py-4 border-b border-white/5 flex items-center gap-3 bg-white/5">
                  <Clock className="w-5 h-5 text-zinc-400" />
                  <h3 className="font-bold">Recent Usage History</h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm text-zinc-400">
                    <thead className="bg-white/5 text-zinc-500 font-medium border-b border-white/5">
                      <tr>
                        <th className="px-6 py-4">Timestamp</th>
                        <th className="px-6 py-4">Model</th>
                        <th className="px-6 py-4">In Tokens</th>
                        <th className="px-6 py-4">Out Tokens</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                      {analytics?.history.map((log, i) => (
                        <tr key={i} className="hover:bg-white/5 transition-colors">
                          <td className="px-6 py-4">{new Date(log.timestamp).toLocaleString()}</td>
                          <td className="px-6 py-4 font-medium text-white">{log.model}</td>
                          <td className="px-6 py-4 text-blue-400">{log.usage.input_tokens}</td>
                          <td className="px-6 py-4 text-purple-400">{log.usage.output_tokens}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </motion.div>
          </main>
        )}
      </div>
    </div>
  );
}
