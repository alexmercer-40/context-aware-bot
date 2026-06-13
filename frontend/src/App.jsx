import { useState, useCallback } from "react";
import { Menu } from "lucide-react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import InputBar from "./components/InputBar";
import FileUpload from "./components/FileUpload";
import { useChat } from "./hooks/useChat";

export default function App() {
  const { messages, isStreaming, currentTool, sendMessage, stop, addSystemMessage } =
    useChat();
  const [uploadOpen, setUploadOpen] = useState(false);
  const [memoryRefreshKey, setMemoryRefreshKey] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleSend = (text) => {
    sendMessage(text);
    setTimeout(() => setMemoryRefreshKey((k) => k + 1), 4000);
  };

  const handleNewChat = () => {
    if (isStreaming) stop();
    window.location.reload();
  };

  const handleUploaded = (res) => {
    addSystemMessage(
      `**${res.filename}** uploaded and indexed (${res.chunks} chunks). You can now ask questions about it.`,
      { type: "upload", filename: res.filename, chunks: res.chunks }
    );
    setMemoryRefreshKey((k) => k + 1);
    setTimeout(() => setUploadOpen(false), 800);
  };

  const toggleSidebar = useCallback(() => setSidebarOpen((v) => !v), []);
  const closeSidebar = useCallback(() => setSidebarOpen(false), []);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950">
      <Sidebar
        onNewChat={handleNewChat}
        refreshKey={memoryRefreshKey}
        isOpen={sidebarOpen}
        onClose={closeSidebar}
      />

      <main className="flex flex-1 flex-col overflow-hidden">
        {/* Mobile top bar */}
        <div className="flex items-center gap-2 border-b border-slate-800 px-3 py-2 md:hidden">
          <button
            onClick={toggleSidebar}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-800 hover:text-slate-200"
          >
            <Menu size={20} />
          </button>
          <span className="text-sm font-medium text-slate-200">Context Chat</span>
        </div>

        <div className="flex-1 overflow-y-auto">
          <ChatWindow
            messages={messages}
            isStreaming={isStreaming}
            currentTool={currentTool}
            onPick={handleSend}
          />
        </div>

        <InputBar
          onSend={handleSend}
          onStop={stop}
          isStreaming={isStreaming}
          onOpenUpload={() => setUploadOpen(true)}
        />
      </main>

      <FileUpload
        open={uploadOpen}
        onClose={() => setUploadOpen(false)}
        onUploaded={handleUploaded}
      />
    </div>
  );
}
