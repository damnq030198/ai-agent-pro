import ChatInterface from '@/components/ChatInterface';
import { LayoutDashboard, MessageSquare, Settings, Database, Activity } from 'lucide-react';

export default function Home() {
  return (
    <main className="flex h-screen bg-[#09090b] text-zinc-100 font-sans selection:bg-blue-500/30">
      {/* Sidebar - Visual only for now */}
      <div className="w-20 lg:w-72 border-r border-white/5 flex flex-col p-4 glass-dark">
        <div className="flex items-center gap-3 px-2 py-4 mb-8">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
            <span className="text-xl font-black text-white">A</span>
          </div>
          <span className="hidden lg:block text-xl font-bold tracking-tight">Agent Pro</span>
        </div>

        <nav className="flex-1 space-y-2">
          <NavItem icon={<MessageSquare size={20} />} label="Hội thoại" active />
          <NavItem icon={<LayoutDashboard size={20} />} label="Thống kê" />
          <NavItem icon={<Database size={20} />} label="Bộ nhớ (RAG)" />
          <NavItem icon={<Activity size={20} />} label="Hệ thống" />
        </nav>

        <div className="mt-auto pt-4 border-t border-white/5 space-y-2">
          <NavItem icon={<Settings size={20} />} label="Cấu hình" />
          <div className="hidden lg:flex items-center gap-3 p-3 rounded-xl bg-white/5 mt-4">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400"></div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-bold truncate">Admin User</p>
              <p className="text-[10px] text-zinc-500 font-medium">Pro Plan</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 relative flex flex-col bg-grid-white/[0.02]">
        {/* Decorative elements */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[128px] -z-10"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-[128px] -z-10"></div>
        
        <div className="flex-1 overflow-hidden p-4 lg:p-8">
          <ChatInterface />
        </div>
      </div>
    </main>
  );
}

function NavItem({ icon, label, active = false }: { icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <div className={`flex items-center gap-4 p-3 rounded-xl cursor-pointer transition-all duration-300 group ${
      active ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20' : 'hover:bg-white/5 text-zinc-400 hover:text-zinc-100'
    }`}>
      <div className="flex-shrink-0">{icon}</div>
      <span className="hidden lg:block text-sm font-semibold tracking-wide">{label}</span>
      {active && <div className="hidden lg:block ml-auto w-1.5 h-1.5 bg-white rounded-full"></div>}
    </div>
  );
}
