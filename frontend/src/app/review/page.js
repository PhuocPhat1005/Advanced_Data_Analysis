"use client";

import {
  Chart as ChartJS,
  TimeScale,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import "chartjs-adapter-date-fns";
import { Bar } from "react-chartjs-2";
import { useEffect, useState } from "react";

import BarChartFilters1 from "../components/review/BarChartFilter1";
import BarChartFilters2 from "../components/review/BarChartFilter2";

import { colorGenerator } from "../utils/getColor";


ChartJS.register(
  CategoryScale,
  TimeScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
  Title
);




export default function ReviewPage() {
  // bar chart 1
  const [selectedColumnBar1, onSelectedColumnBar1] = useState(null);
  const [selectedMethods, onMethodChange] = useState([{ value: "sum", labels: "Sum" }]);
  const [selectedCategoriesBar1, onCategoriesBar1Change] = useState([]);
  const [detailedCategoriesBar1, ondetailedCategoriesBar1Change] = useState([]);
  const [rawBar1Data, setRawBar1Data] = useState([]);
  const [bar1Data, setBar1Data] = useState({ labels: [], datasets: [] });
  const methodsOption = [
    { value: "sum", label: "Sum" },
    { value: "mean", label: "Mean" }
  ]

  // bar chart 2
  const [selectedColumnBar2, onSelectedColumnBar2] = useState([]);
  const [selectedCategoriesBar2, onCategoriesBar2Change] = useState([]);
  const [detailedCategoriesBar2, ondetailedCategoriesBar2Change] = useState([]);
  const [rawBar2Data, setRawBar2Data] = useState([]);
  const [bar2Data, setBar2Data] = useState({ labels: [], datasets: [] });


  // both bar
  const columnOptions = [
    { value: "product_source", label: "Product Source" },
    { value: "category", label: "Category" },
    { value: "current_seller", label: "Current Seller" },
  ];


  // Bar 1 fetch
  useEffect(() => {
    const fetchRawDataBar1 = async () => {
      if (!selectedColumnBar1 || !selectedMethods) return;

      try {
        const res = await fetch(
          `http://127.0.0.1:8000/analysis/descriptive/ratings/reviews/count/by-factor?factor_column=${selectedColumnBar1.value}&by_function=${selectedMethods.value}`
        );
        const json = await res.json();
        if (Array.isArray(json.records)) {
          setRawBar1Data(json.records);

          // Cập nhật filter options
          const uniqueCats = [...new Set(json.records.map(r => r[selectedColumnBar1.value]))];
          ondetailedCategoriesBar1Change(uniqueCats.map(val => ({ value: val, label: val })));
        }
      } catch (err) {
        console.error("Fetch failed:", err);
      }
    };

    fetchRawDataBar1();
  }, [selectedColumnBar1, selectedMethods]);

  // Bar 1 filter
  useEffect(() => {
    if (!selectedCategoriesBar1 || selectedCategoriesBar1.length === 0) return;
    if (!rawBar1Data || rawBar1Data.length === 0) return;
    if (!selectedColumnBar1) return;

    const key = selectedColumnBar1.value;
    const resultKey = selectedMethods.value === "mean" ? "review_count_mean" : "review_count_sum";

    const colorGen = colorGenerator();

    const datasets = selectedCategoriesBar1.map(cat => {
      const total = rawBar1Data
        .filter(r => r[key] === cat.value)
        .reduce((sum, r) => sum + (r[resultKey] || 0), 0);

      return {
        label: cat.label,
        data: [total],
        backgroundColor: colorGen.next().value,
      };
    });

    setBar1Data({
      labels: [""],
      datasets,
    });
  }, [selectedCategoriesBar1, rawBar1Data, selectedColumnBar1, selectedMethods]);


  // Bar 2 fetch
  useEffect(() => {
    const fetchRawDataBar2 = async () => {
      if (!selectedColumnBar2) return;

      try {
        const res = await fetch(
          `http://127.0.0.1:8000/analysis/descriptive/ratings/average/by-factors?factor_columns=${selectedColumnBar2.value}`
        );
        const json = await res.json();
        if (Array.isArray(json.records)) {
          setRawBar2Data(json.records);

          // Cập nhật filter options
          const uniqueCats = [...new Set(json.records.map(r => r[selectedColumnBar2.value]))];
          ondetailedCategoriesBar2Change(uniqueCats.map(val => ({ value: val, label: val })));
        }
      } catch (err) {
        console.error("Fetch failed:", err);
      }
    };

    fetchRawDataBar2();
  }, [selectedColumnBar2]);

  // Bar 2 filter
  useEffect(() => {
    if (!selectedCategoriesBar2 || selectedCategoriesBar2.length === 0) return;
    if (!rawBar2Data || rawBar2Data.length === 0) return;
    if (!selectedColumnBar2) return;

    const key = selectedColumnBar2.value;
    const colorGen = colorGenerator();

    const datasets = selectedCategoriesBar2.map(cat => {
      const recordsForCategory = rawBar2Data.filter(r => r[key] === cat.value);

      const avg = recordsForCategory.reduce((sum, r) => sum + (r.avg_rating || 0), 0) / recordsForCategory.length || 0;

      return {
        label: cat.label,
        data: [avg],
        backgroundColor: colorGen.next().value,
      };
    });

    setBar2Data({
      labels: [""],
      datasets,
    });
  }, [selectedCategoriesBar2, selectedColumnBar2, rawBar2Data]);


  // bar options
  const bar1Options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: `Phân loại số lượt đánh giá`,
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Số lượng đánh giá (đơn vị: lượt)",
        },
      },
      y: {
        title: {
          display: true,
          text: "Phân loại",
        },
      },
    },
  };

  // bar options
  const bar2Options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: `Phân loại mức độ đánh giá`,
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Số sao đánh giá",
        },
      },
      y: {
        title: {
          display: true,
          text: "Phân loại",
        },
      },
    },
  };

  return (
    <div className="p-6 min-h-[calc(100vh-50px)]  overflow-hidden flex flex-col">
      <h1 className="text-2xl font-bold mb-4">PHÂN TÍCH SỐ SAO ĐÁNH GIÁ VÀ SỐ LƯỢT ĐÁNH GIÁ</h1>
      <div className="flex flex-col gap-6 ">
        {/* Bar Chart 1 Section */}
        <div className="bg-white shadow p-4 rounded-lg h-[610px] w-full">
          <BarChartFilters1
            selectedColumn={selectedColumnBar1}
            onColumnChange={onSelectedColumnBar1}
            selectedMethods={selectedMethods}
            onMethodChange={onMethodChange}
            selectedCategories={selectedCategoriesBar1}
            onCategoriesChange={onCategoriesBar1Change}
            dataOptions={detailedCategoriesBar1}
            columnOptions={columnOptions}
            methodOptions={methodsOption}
          />

          <div className="mt-6 h-[500px] relative">
            <Bar data={bar1Data} options={bar1Options} />
          </div>
        </div>

        <div className="bg-white shadow p-4 rounded-lg h-[610px] w-full">
          <BarChartFilters2
            selectedColumn={selectedColumnBar2}
            onColumnChange={onSelectedColumnBar2}
            selectedCategories={selectedCategoriesBar2}
            onCategoriesChange={onCategoriesBar2Change}
            dataOptions={detailedCategoriesBar2}
            columnOptions={columnOptions}
          />
          <div className="mt-6 h-[500px] relative">
            <Bar data={bar2Data} options={bar2Options}></Bar>
          </div>
        </div>
      </div>
    </div>
  );
}