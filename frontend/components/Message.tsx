"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import SourceCard from "./SourceCard";

type Source = {
  type: string;
  chapter: number;
  verse?: number;
  topic?: string;
};

type Props = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export default function Message({
  role,
  content,
  sources = [],
}: Props) {

  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>

      <div
        className={`max-w-2xl rounded-3xl p-5 shadow ${
          isUser
            ? "bg-orange-100"
            : "bg-white"
        }`}
      >

        {isUser ? (
          <p>{content}</p>
        ) : (
          <>
            <div className="prose prose-slate max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {content}
              </ReactMarkdown>
            </div>

            {/* <SourceCard sources={sources} /> */}
          </>
        )}

      </div>

    </div>
  );
}