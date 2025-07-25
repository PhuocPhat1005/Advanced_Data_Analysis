import React from "react";

export default function prettifyLLMResult(result) {
  if (!result) return null;

  // Chuyển tất cả \n về xuống dòng thật nếu là chuỗi escaped
  const normalized = result.replace(/\\n/g, "\n");

  const paragraphs = normalized.split(/\n\s*\n/); // tách đoạn

  return (
    <div className="space-y-3 text-gray-800 leading-relaxed">
      {paragraphs.map((para, idx) => {
        // nếu là danh sách đánh số
        if (/^\d+\.\s/.test(para)) {
          const lines = para.split("\n").filter(line => line.trim());
          return (
            <ol key={idx} className="list-decimal list-inside space-y-1">
              {lines.map((line, i) => {
                const clean = line.replace(/^\d+\.\s/, "");
                return (
                  <li key={i} dangerouslySetInnerHTML={{ __html: formatInline(clean) }} />
                );
              })}
            </ol>
          );
        }

        return (
          <p key={idx} dangerouslySetInnerHTML={{ __html: formatInline(para) }} />
        );
      })}
    </div>
  );
}

function formatInline(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // **bold**
    .replace(/"([^"]+)"/g, '<span style="color:#2563eb;">"$1"</span>') // highlight "
    .replace(/[“”]/g, '"'); // normalize “”
}