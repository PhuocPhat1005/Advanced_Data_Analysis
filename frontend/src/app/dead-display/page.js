"use client";

import { useId, useState } from "react";
import Select from "react-select";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import prettifyLLMResult from "../utils/llmPrettier";

const columnOptions = [
  { value: "brand", label: "Brand" },
  { value: "category", label: "Category" },
  { value: "has_video", label: "Has Video" },
  { value: "number_of_images", label: "Number Of Images" },
  { value: "name_length", label: "Name Length" },
  { value: "original_price", label: "Original Price" },
];

export default function BadReviewsPage() {
  const [selectedRange, onRangeChange] = useState([new Date("2016-01-01"), null]);
  const [selectedColumns, setSelectedColumns] = useState([]);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [llmResult, setLlmResult] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);
  const [expanded, setExpanded] = useState(false);

  const selectId = useId();

  const handleRunAnalysis = async () => {
    if (!selectedRange[0] || !selectedRange[1] || !selectedColumns || selectedColumns.length === 0) {
      alert("Please select at least one column or date range");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/analysis/diagnostic/status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          factor_groups: selectedColumns.map((col) => col.value),
          min_date: selectedRange[0].toISOString().slice(0, 10),
          max_date: selectedRange[1].toISOString().slice(0, 10),
        }),
      });

      if (!response.ok) throw new Error("Failed to fetch analysis data");

      const result = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      console.error(err);
      alert("Error running analysis.");
    }
  };

  const handleLLMAnalyze = async () => {
    try {
      const formData = new FormData();
      const jsonBlob = new Blob([JSON.stringify(analysisResult, null, 2)], {
        type: "application/json",
      });
      formData.append("file", jsonBlob, "status_reason.json");

      const res = await fetch("http://127.0.0.1:8000/analysis/diagnostic/status/llm", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.text();
        throw new Error(err || "Request failed");
      }

      const result = await res.text();
      setLlmResult(result);
    } catch (error) {
      console.error("LLM Analyze Error:", error);
      alert("LLM request failed. Check console.");
    }
  };

  const handleLLMAnalyzeFromFile = async () => {
    if (!uploadedFile) {
      alert("Please upload a dataset file first.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", uploadedFile);

      const res = await fetch("http://127.0.0.1:8000/analysis/diagnostic/status/llm", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.text();
        throw new Error(err || "Request failed");
      }

      const result = await res.text();
      setLlmResult(result);
    } catch (error) {
      console.error("LLM File Analyze Error:", error);
      alert("LLM file request failed. Check console.");
    }
  };

  return (
    <div className="p-6 min-h-[calc(100vh-50px)] bg-gray-50 overflow-hidden">
      <h1 className="text-2xl font-bold mb-4">PHÂN TÍCH NGUYÊN NHÂN TRƯNG BÀY CHẾT</h1>
      {/* Controls */}

      <div className="mb-6 rounded-lg bg-white shadow p-4 w-full flex flex-row items-end justify-between gap-4">
        {/* Select Columns */}
        <div className="flex-1 min-w-[250px]">
          <label htmlFor={selectId} className="block text-sm font-medium mb-1">
            Select Factor Columns
          </label>
          <Select
            instanceId={selectId}
            inputId={selectId}
            isMulti
            options={columnOptions}
            value={selectedColumns}
            onChange={setSelectedColumns}
            className="text-sm"
          />
        </div>

        {/* Date Range Picker */}
        <div className="flex flex-col min-w-[200px]">
          <label className="block text-sm font-medium mb-1">Select Date Range</label>
          <DatePicker
            selectsRange
            startDate={selectedRange[0]}
            endDate={selectedRange[1]}
            onChange={(update) =>
              onRangeChange(Array.isArray(update) ? update : [null, null])
            }
            dateFormat="yyyy-MM-dd"
            showMonthDropdown
            showYearDropdown
            dropdownMode="select"
            minDate={new Date("2016-01-01")}
            className="border px-2 py-1 rounded-lg"
            placeholderText="Chọn khoảng thời gian"
          />
        </div>

        {/* Button */}
        <div className="flex-shrink-0">
          <button
            onClick={handleRunAnalysis}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Phân tích
          </button>
        </div>
      </div>




      {/* Upload CSV for LLM */}
      <div className="mb-6">
        <label className="block font-medium mb-1">Upload json để LLM phân tích (Tùy Chọn)</label>
        <input
          className="underline cursor-pointer"
          type="file"
          accept=".json"
          onChange={(e) => setUploadedFile(e.target.files?.[0] || null)}
        />
        <button
          onClick={handleLLMAnalyzeFromFile}
          className="mt-2 bg-indigo-600 text-white px-4 py-1 rounded-lg hover:bg-indigo-700"
          disabled={!uploadedFile}
        >
          Phân tích JSON bằng LLM
        </button>
      </div>

      {/* Analysis Result */}
      {analysisResult && (
        <div className="bg-white shadow p-4 rounded-lg mb-6">
          <h2 className="font-semibold mb-2">Analysis Result (JSON)</h2>
          <pre className="bg-gray-100 p-2 rounded-lg text-sm overflow-x-auto max-h-[400px]">
            {expanded
              ? JSON.stringify(analysisResult, null, 2)
              : JSON.stringify(analysisResult, null, 2).split("\n").slice(0, 20).join("\n") + "\n..."}
          </pre>

          <button
            className="text-blue-600 underline text-sm mt-1"
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? "Ẩn bớt" : "Xem thêm"}
          </button>

          <button
            className="mt-3 bg-green-600 text-white px-4 py-1 rounded-lg hover:bg-green-700 ml-4"
            onClick={() => {
              const blob = new Blob([JSON.stringify(analysisResult, null, 2)], {
                type: "application/json",
              });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = "status_reason.json";
              a.click();
            }}
          >
            Download Result
          </button>
        </div>
      )}

      {/* LLM Explanation */}
      {(analysisResult || llmResult) && (
        <div className="bg-white shadow p-4 rounded-lg">
          <h2 className="font-semibold mb-2">Trợ lý LLM</h2>
          {analysisResult && (
            <button
              onClick={handleLLMAnalyze}
              className="bg-purple-600 text-white px-4 py-1 rounded-lg hover:bg-purple-700 mb-2"
            >
              Phân tích kết quả trả về với LLM
            </button>
          )}
          {llmResult && prettifyLLMResult(llmResult)}
        </div>
      )}
    </div>
  );
}