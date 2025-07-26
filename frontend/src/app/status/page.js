"use client"

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
import "react-datepicker/dist/react-datepicker.css";
import { useEffect, useState } from "react";

import BarChartFilters from "../components/status/BarChartFilters";
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

export default function StatusPage() {
  const [selectedRange, onRangeChange] = useState([new Date('2016-01-01'), null]);
  const [selectedColumn, onSelectedColumn] = useState(null);
  const [selectedCategories, onCategoriesChange] = useState([]);
  const [detailedCategories, ondetailedCategoriesChange] = useState([]);
  const [selectedStatus, onStatusChange] = useState([])
  const [rawData, setRawData] = useState([]);
  const [data, setData] = useState({ labels: [], datasets: [] });

  const columnOptions = [
    { value: "product_source", label: "Product Source" },
    { value: "category", label: "Category" },
    { value: "current_seller", label: "Current Seller" },
  ];

  const statusOptions = [
    { value: "0", label: "Không khả thi" },
    { value: "1", label: "Khả thi" }
  ];


  // Fetch
  useEffect(() => {
    const fetchDetailedCategories = async () => {
      if (!selectedColumn || !selectedRange?.[0] || !selectedRange?.[1]) return;

      const minDate = selectedRange[0].toISOString().slice(0, 10);
      const maxDate = selectedRange[1].toISOString().slice(0, 10);

      const statusValues = selectedStatus.map((s) => s.value);

      const statusParams = statusValues.map(s => `status=${s}`).join("&");

      const url = `http://127.0.0.1:8000/analysis/descriptive/status/display/by-factor?factor_column=${selectedColumn.value}&min_date=${minDate}&max_date=${maxDate}${statusParams ? '&' + statusParams : ''}`;

      try {
        const res = await fetch(url);
        const json = await res.json();

        const uniqueValues = [...new Set(json.records.map((r) => r[selectedColumn.value]))];
        const options = uniqueValues.map((val) => ({ value: val, label: val }));

        ondetailedCategoriesChange(options);
      } catch (err) {
        console.error("Failed to fetch detailed column data:", err);
      }
    };

    fetchDetailedCategories();
  }, [selectedColumn, selectedRange, selectedStatus]);

  // Filter
  useEffect(() => {
    if (!selectedColumn || !selectedRange?.[0] || !selectedRange?.[1]) return;
    if (!selectedCategories.length) return;
    if (!selectedStatus.length) return;

    const fetchChartData = async () => {
      const minDate = selectedRange[0].toISOString().split("T")[0];
      const maxDate = selectedRange[1].toISOString().split("T")[0];
      const statusValues = selectedStatus.map((s) => s.value);
      const statusParams = statusValues.map(s => `status=${s}`).join("&");

      const url = `http://127.0.0.1:8000/analysis/descriptive/status/display/by-factor?factor_column=${selectedColumn.value}&min_date=${minDate}&max_date=${maxDate}${statusParams ? '&' + statusParams : ''}`;

      try {
        const res = await fetch(url);
        const json = await res.json();
        setRawData(json.records);

        const key = selectedColumn.value;
        const selectedValues = selectedCategories.map((c) => c.value);

        const filtered = json.records.filter(
          (r) =>
            selectedValues.includes(r[key]) &&
            statusValues.includes(String(r.status))
        );

        // Lấy tất cả giá trị duy nhất từ `selectedColumn`
        const labels = [...new Set(filtered.map((r) => r[key]))];

        const datasets = statusValues.map((sVal) => {
          const color = colorGenerator();
          return {
            label: statusOptions.find((opt) => opt.value === sVal)?.label || sVal,
            data: labels.map((label) => {
              const found = filtered.find(
                (r) => r[key] === label && String(r.status) === sVal
              );
              return found ? found.count : 0;
            }),
            backgroundColor: sVal === '1' ? "#F0561D" : "#DCA614",
          };
        });

        setData({ labels, datasets });
      } catch (err) {
        console.error("Failed to fetch chart data:", err);
      }
    };

    fetchChartData();
  }, [selectedColumn, selectedCategories, selectedRange, selectedStatus]);

  const options = {
    indexAxis: 'y', // <- Đây là dòng quan trọng để xoay bar chart nằm ngang
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Số lượng theo phân loại và trạng thái",
        font: {
          size: 18,
          weight: "bold"
        }
      },
      legend: {
        position: "top",
        labels: {
          boxWidth: 20,
          padding: 15,
        },
      },
      tooltip: {
        mode: "index",
        intersect: false,
        callbacks: {
          label: function (context) {
            const label = context.dataset.label || '';
            const value = context.parsed.x || 0; // Lưu ý: dùng `.x` thay vì `.y` vì trục đã xoay
            return `${label}: ${value} mục`;
          }
        }
      },
    },
    interaction: {
      mode: "nearest",
      axis: "y",
      intersect: false,
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Số lượng sản phẩm (đơn vị: cái)",
        },
        ticks: {
          stepSize: 1,
        },
      },
      y: {
        title: {
          display: true,
          text: "Phân loại",
        },
        ticks: {
          autoSkip: false,
          maxRotation: 0,
          minRotation: 0,
        },
      },
    },
  };


  return (
    <div className="p-6 min-h-[calc(100vh-50px)]  overflow-hidden flex flex-col">
      <h1 className="text-2xl font-bold mb-4">PHÂN TÍCH TÌNH TRẠNG</h1>
      <div className="flex flex-col gap-6 ">
        {/* Bar Chart 1 Section */}
        <div className="bg-white shadow p-4 rounded-lg h-[610px] w-full">
          <BarChartFilters
            selectedRange={selectedRange}
            onRangeChange={onRangeChange}
            selectedColumn={selectedColumn}
            onColumnChange={onSelectedColumn}
            selectedCategories={selectedCategories}
            onCategoriesChange={onCategoriesChange}
            dataOptions={columnOptions}
            detailedColumnData={detailedCategories}
            selectedOptions={selectedStatus}
            onOptionsChange={onStatusChange}
            options={statusOptions}
          />

          <div className="mt-6 h-[500px] relative">
            <Bar data={data} options={options} />
          </div>
        </div>
      </div>
    </div>
  );
}