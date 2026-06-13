import { useRef, useState } from "react";
import { Send, Square, Paperclip } from "lucide-react";

export default function InputBar({ onSend, onStop, isStreaming, onOpenUpload }) {
  const [value, setValue] = useState("");
  const textareaRef = useRef(null);

  const autoGrow = (el) => {
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 180)}px`;
  };

  const submit = () => {
    const text = value.trim();
    if (!text || isStreaming) return;
    onSend(text);
    setValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div className="mx-auto w-full max-w-3xl px-4 pb-5">
      <div className="flex items-end gap-2 rounded-2xl border border-slate-700/80 bg-slate-800/70 p-2 shadow-lg backdrop-blur">
        <button
          onClick={onOpenUpload}
          title="Upload a document"
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-700/60 hover:text-slate-200"
        >
          <Paperclip size={18} />
        </button>

        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            autoGrow(e.target);
          }}
          onKeyDown={handleKeyDown}
          placeholder="Send a message…  (Enter to send, Shift+Enter for newline)"
          className="max-h-44 flex-1 resize-none bg-transparent px-2 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none"
        />

        {isStreaming ? (
          <button
            onClick={onStop}
            title="Stop generating"
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-700 text-slate-100 transition hover:bg-slate-600"
          >
            <Square size={16} fill="currentColor" />
          </button>
        ) : (
          <button
            onClick={submit}
            disabled={!value.trim()}
            title="Send"
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white transition enabled:hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <Send size={16} />
          </button>
        )}
      </div>
      <p className="mt-2 text-center text-[11px] text-slate-600">
        The assistant remembers facts you share across the conversation.
      </p>
    </div>
  );
}
