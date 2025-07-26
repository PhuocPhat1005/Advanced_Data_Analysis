"use client";

import { useRef, useEffect, useState } from "react";
import { PiRobot } from "react-icons/pi";
import { FiSend } from "react-icons/fi";
import axios from "axios";

export default function AssistantPage() {
  const [messages, setMessages] = useState([
    { type: "bot", text: "Xin chào! Tôi có thể giúp gì cho bạn về dữ liệu?" },
  ]);
  const [input, setInput] = useState("");
  const [availableDatasets, setAvailableDatasets] = useState([]);
  const [uploadedDatasets, setUploadedDatasets] = useState([]);

  // scroll to bottom
  const bottomRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // animated text
  const [animatedText, setAnimatedText] = useState(""); // text đang hiển thị từ từ

  const typeText = (fullText, callback) => {
    let index = 0;
    const speed = 5;

    const type = () => {
      if (index <= fullText.length) {
        setAnimatedText(fullText.slice(0, index));
        index++;
        setTimeout(type, speed);
      } else {
        callback?.();
      }
    };

    type();
  };

  // Load default datasets on first render
  useEffect(() => {
    const loaded = sessionStorage.getItem("llm_defaults_loaded");
    if (loaded) return;

    const fetchDefaults = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/ai_agent/llm_agent/defaults");
        setAvailableDatasets(res.data.map((d) => d.name));
        res.data.forEach((d) => {
          setMessages((prev) => [
            ...prev,
            { type: "bot", text: `Đã tải dữ liệu: ${d.name}\nMô tả: ${d.summary}` },
          ]);
        });
        sessionStorage.setItem("llm_defaults_loaded", "true");
      } catch (err) {
        console.error("Lỗi khi tải datasets mặc định:", err);
        setMessages((prev) => [
          ...prev,
          { type: "bot", text: "Không thể tải dữ liệu mặc định. Vui lòng thử lại sau." },
        ]);
      }
    };

    fetchDefaults();
  }, []);


  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { type: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/ai_agent/llm_agent/ask", {
        model: "gemini-2.5-flash",
        prompt_type: "preset",
        custom_prompt: "",
        preset_key: "overview",
        user_query: input,
        df_names: [...availableDatasets, ...uploadedDatasets],
      });

      const botResponse = res.data.answer || "Không có phản hồi.";

      setAnimatedText("");
      typeText(botResponse, () => {
        setMessages((prev) => [...prev, { type: "bot", text: botResponse }]);
        setAnimatedText("");
      });

    } catch (err) {
      console.error("Lỗi khi gửi câu hỏi:", err);
      setMessages((prev) => [...prev, { type: "bot", text: "Đã xảy ra lỗi khi phản hồi. Vui lòng thử lại." }]);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !file.name.endsWith(".csv")) return;

    const reader = new FileReader();
    reader.onload = async (event) => {
      const csvContent = event.target.result;
      const dfName = file.name;

      try {
        await axios.post("http://127.0.0.1:8000/ai_agent/llm_agent/upload", {
          df_name: dfName,
          csv_content: csvContent,
        });

        setUploadedDatasets((prev) => [...prev, dfName]);
        setMessages((prev) => [
          ...prev,
          { type: "bot", text: `Đã tải lên dữ liệu người dùng: ${dfName}` },
        ]);
      } catch (err) {
        console.error("Lỗi khi upload:", err);
        setMessages((prev) => [...prev, { type: "bot", text: "Tải dữ liệu thất bại. Vui lòng thử lại." }]);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="h-full flex flex-col p-6">
      <div className="flex items-center gap-2 mb-4 text-2xl font-semibold">
        <PiRobot className="text-blue-600" /> Trợ lý dữ liệu
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 p-4 bg-gray-50 rounded-2xl border border-cyan-600">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`max-w-[80%] px-4 py-2 rounded-xl text-sm shadow-sm whitespace-pre-wrap
      ${msg.type === "user" ? "ml-auto bg-blue-100 text-blue-800 font-bold" : "bg-white border border-cyan-600 text-gray-800 font-semibold"}`}
          >
            {msg.text}
          </div>
        ))}

        {/* render đoạn typing riêng nếu đang có animatedText */}
        {animatedText && (
          <div className="max-w-[80%] px-4 py-2 rounded-xl text-sm shadow-sm whitespace-pre-wrap bg-white border border-cyan-600 text-gray-800 font-semibold">
            {animatedText}
          </div>
        )}
        <div ref={bottomRef} />

      </div>

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
        <label className="bg-green-600 hover:bg-green-800 text-white px-3 py-2 rounded-2xl cursor-pointer">
          Upload CSV
          <input type="file" accept=".csv" className="hidden" onChange={handleFileUpload} />
        </label>
      </div>
    </div>
  );
}
