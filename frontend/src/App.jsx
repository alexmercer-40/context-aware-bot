import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import InputBar from "./components/InputBar";
import FileUpload from "./components/FileUpload";
import { useChat } from "./hooks/useChat";

export default function App() {
  const { messages, isStreaming, currentTool, sendMessage, stop } = useChat();
  const [uploadOpen, setUploadOpen] = useState(false);
  const [memoryRefreshKey, setMemoryRefreshKey] = useState(0);

  const handleSend = (text) => {
    sendMessage(text);
    // After the agent likely saved/updated memory, refresh the sidebar shortly after.
    setTimeout(() => setMemoryRefreshKey((k) => k + 1), 4000);
  };

  const handleNewChat = () => {
    if (isStreaming) stop();
    // Reloading resets in-memory chat state; long-term memory persists in the DB.
    window.location.reload();
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950">
      <Sidebar onNewChat={handleNewChat} refreshKey={memoryRefreshKey} />

      <main className="flex flex-1 flex-col overflow-hidden">
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
        onUploaded={() => setMemoryRefreshKey((k) => k + 1)}
      />
    </div>
  );
}
