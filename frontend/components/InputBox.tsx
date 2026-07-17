"use client";

import { useState } from "react";
import { SendHorizontal } from "lucide-react";

type Props = {
  onSend: (message: string) => void;
  loading: boolean;
};

export default function InputBox({ onSend, loading }: Props) {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim()) return;

    onSend(message);
    setMessage("");
  };

  return (
    <div className="flex items-center gap-3 rounded-3xl border bg-white p-3 shadow-lg">

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSend();
        }}
        placeholder="Share what's on your mind..."
        className="flex-1 outline-none px-3 text-lg"
      />

      <button
        disabled={loading}
        onClick={handleSend}
        className="rounded-full bg-orange-400 p-3 text-white hover:bg-orange-500 disabled:opacity-50"
      >
        <SendHorizontal size={18} />
      </button>

    </div>
  );
}