"use client"
import { useState } from "react";
import { PiRobot } from "react-icons/pi";
import { FiSend } from "react-icons/fi";

export default function AssistantPage() {
  const [messages, setMessages] = useState([
    { type: "bot", text: "Xin chào! Tôi có thể giúp gì cho bạn về dữ liệu?" },
  ]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) {
      return;
    }

    const newUserMsg = { type: "user", text: input };

    setMessages((prev) => [...prev, newUserMsg]);
    setInput("");

    // Fake response (replace with real API call)
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: `Tôi đang phân tích: "${input}"... (trả lời mẫu)`,
        },
      ]);
    }, 1000);
  };

  return (
    <div className="h-full flex flex-col p-6">
      <div className="flex items-center gap-2 mb-4 text-2xl font-semibold">
        <PiRobot className="text-blue-600" /> Trợ lý dữ liệu
      </div>
      {/* outer frame */}

      <div className="flex-1 overflow-y-auto space-y-4 p-4 bg-gray-50 rounded-2xl border border-cyan-600">
        {messages.map((msg, index) => (
          // message frame
          <div
            key={index}
            className={`max-w-[80%] px-4 py-2 rounded-xl text-sm shadow-sm whitespace-pre-wrap
              ${msg.type === "user" ? "ml-auto bg-blue-100 text-blue-800 font-bold" : "bg-white border border-cyan-600 text-gray-800 font-semibold"}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      {/*  input frame */}
      <div className="mt-4 flex items-center gap-2">
        <input
          type="text"
          placeholder="Hỏi gì đó về dữ liệu..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          className="flex-1 border border-cyan-600 px-4 py-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 hover:bg-blue-800 text-white p-2 rounded-2xl"
        >
          <FiSend className="text-xl" />
        </button>
      </div>
    </div>
  );
}
