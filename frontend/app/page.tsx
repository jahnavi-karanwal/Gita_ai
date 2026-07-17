"use client";

import { useState } from "react";

import Navbar from "@/components/Navbar";
import InputBox from "@/components/InputBox";
import SuggestionCard from "@/components/SuggestionCard";
import Message from "@/components/Message";


import { sendMessage } from "@/lib/api";

export default function Home() {

  type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: {
    type: string;
    chapter: number;
    verse?: number;
    topic?: string;
  }[];
};

const [messages, setMessages] = useState<Message[]>([]);

  const [loading, setLoading] = useState(false);

  const suggestions = [
    "🌿 I feel anxious",
    "💼 Placement stress",
    "❤️ Relationship advice",
    "📖 Explain Karma Yoga",
    "🌱 Finding purpose",
  ];

  async function handleSend(message: string) {

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: message,
      },
    ]);

    setLoading(true);

    try {

      const res = await sendMessage(message);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.answer,
          sources: res.sources,
        },
      ]);

    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#FFFDF8] px-6">

      <div className="max-w-5xl mx-auto">

        <Navbar
        onNewChat={() => setMessages([])}
        />

        {messages.length === 0 ? (

          <div className="max-w-3xl mx-auto text-center mt-20">

            <h1 className="text-6xl">🪷</h1>

            <h1 className="text-5xl font-bold mt-4">
              KrishnaGPT
            </h1>

            <p className="mt-3 text-slate-500">
              Wisdom from the Bhagavad Gita for everyday life.
            </p>

            <div className="mt-10">
              <InputBox
                onSend={handleSend}
                loading={loading}
              />
            </div>

            <div className="grid grid-cols-2 gap-4 mt-8">

              {suggestions.map((item) => (
                <SuggestionCard
                key={item}
                text={item}
                onClick={() => handleSend(item)}
                />
                ))}

            </div>

          </div>

        ) : (

          <div className="max-w-3xl mx-auto py-10">

            <div className="space-y-8">

              {messages.map((msg, index) => (
                <Message
                  key={index}
                  role={msg.role}
                  content={msg.content}
                  sources={msg.sources}
                />
              ))}
            

              {loading && (
                <p className="text-slate-500">
                  🌿 Reflecting...
                </p>
              )}

            </div>

            <div className="sticky bottom-6 mt-10">

              <InputBox
                onSend={handleSend}
                loading={loading}
              />

            </div>

          </div>

        )}

      </div>

    </main>
  );
}