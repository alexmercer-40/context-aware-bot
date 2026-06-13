import { Brain, Save, Trash2, FileSearch, Loader2 } from "lucide-react";

// Map tool names to a friendly label + icon.
const TOOL_META = {
  save_memory: { label: "Saving to memory", Icon: Save },
  search_memory: { label: "Searching memory", Icon: Brain },
  delete_memory: { label: "Updating memory", Icon: Trash2 },
  search_document: { label: "Searching documents", Icon: FileSearch },
};

export default function ToolIndicator({ tool }) {
  if (!tool) return null;
  const meta = TOOL_META[tool] || { label: `Using ${tool}`, Icon: Loader2 };
  const { label, Icon } = meta;

  return (
    <div className="flex animate-fade-in items-center gap-2 self-start rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-300">
      <Icon size={14} className="animate-pulse-soft" />
      <span>{label}…</span>
    </div>
  );
}
