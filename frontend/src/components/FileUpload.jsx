import { useRef, useState } from "react";
import { X, UploadCloud, FileText, CheckCircle2, Loader2 } from "lucide-react";
import { uploadDocument } from "../api/chatApi";

export default function FileUpload({ open, onClose, onUploaded }) {
  const [dragging, setDragging] = useState(false);
  const [status, setStatus] = useState("idle"); // idle | uploading | done | error
  const [message, setMessage] = useState("");
  const inputRef = useRef(null);

  if (!open) return null;

  const handleFile = async (file) => {
    if (!file) return;
    setStatus("uploading");
    setMessage(file.name);
    try {
      const res = await uploadDocument(file);
      setStatus("done");
      setMessage(`${res.filename} — ${res.chunks} chunks indexed`);
      onUploaded?.(res);
    } catch (err) {
      setStatus("error");
      setMessage(err.message || "Upload failed");
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  const reset = () => {
    setStatus("idle");
    setMessage("");
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-base font-semibold text-slate-100">
            Upload a document
          </h3>
          <button
            onClick={onClose}
            className="text-slate-400 transition hover:text-slate-200"
          >
            <X size={18} />
          </button>
        </div>

        {status === "done" ? (
          <div className="flex flex-col items-center gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 py-8 text-center">
            <CheckCircle2 size={32} className="text-emerald-400" />
            <p className="px-4 text-sm text-emerald-200">{message}</p>
            <button
              onClick={reset}
              className="mt-1 rounded-lg border border-slate-600 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-800"
            >
              Upload another
            </button>
          </div>
        ) : (
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => status !== "uploading" && inputRef.current?.click()}
            className={`flex cursor-pointer flex-col items-center gap-3 rounded-xl border-2 border-dashed py-10 text-center transition ${
              dragging
                ? "border-indigo-500 bg-indigo-500/10"
                : "border-slate-700 hover:border-slate-600"
            }`}
          >
            {status === "uploading" ? (
              <>
                <Loader2 size={30} className="animate-spin text-indigo-400" />
                <p className="text-sm text-slate-300">Processing {message}…</p>
              </>
            ) : (
              <>
                <UploadCloud size={30} className="text-slate-400" />
                <p className="text-sm text-slate-300">
                  Drag &amp; drop a PDF or text file
                </p>
                <p className="text-xs text-slate-500">or click to browse</p>
              </>
            )}
            <input
              ref={inputRef}
              type="file"
              accept=".pdf,.txt,.md"
              className="hidden"
              onChange={(e) => handleFile(e.target.files?.[0])}
            />
          </div>
        )}

        {status === "error" && (
          <p className="mt-3 flex items-center gap-2 text-xs text-rose-400">
            <FileText size={14} /> {message}
          </p>
        )}
      </div>
    </div>
  );
}
