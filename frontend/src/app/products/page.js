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
import "react-datepicker/dist/react-datepicker.css";

import { colorGenerator } from "../utils/getColor";
import { useState, useEffect } from "react";
import BarChartFilters1 from "../components/products/BarChartFilters1";

ChartJS.register(
  TimeScale,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
  Title
);


export default function ProductPage() {
  // bar chart data 1

  const [selectedRange, onRangeChange] = useState([new Date("2016-01-01"), null]);
  const [selectedColumns, onColumnsChange] = useState([]);
  const [detailedColumnData, onDetailedColumnDataChange] = useState([]);
  const [selectedCategories, onCategoriesChange] = useState([]);
  const [rawRecordsBar1, setRawRecordsBar1] = useState([]);
  const [bar1Data, setBar1Data] = useState({ labels: [], datasets: [] });


  const columnOptions = [
    { value: "category", label: "Category" },
    { value: "product_source", label: "Product Source" },
  ];

  useEffect(() => {
    const fetchData = async () => {
      if (
        !selectedRange?.[0] ||
        !selectedRange?.[1] ||
        !selectedColumns?.length
      ) {
        console.log("Missing date range or selected columns");
        return;
      }

      const minDate = selectedRange[0].toISOString().slice(0, 10);
      const maxDate = selectedRange[1].toISOString().slice(0, 10);
      const factorGroupColumns = selectedColumns.map(col => col.value).join(",");

      const url = `http://127.0.0.1:8000/analysis/descriptive/products/quantity/grouped?factor_group_columns=${factorGroupColumns}&min_date=${minDate}&max_date=${maxDate}`;

      try {
        const res = await fetch(url);
        const json = await res.json();
        console.log("Fetched records: ", json);

        if (Array.isArray(json.records)) {
          setRawRecordsBar1(json.records);

          const currentCol = selectedColumns[0]?.value;
          const uniqueValues = Array.from(
            new Set(json.records.map(r => r[currentCol]))
          );
          const options = uniqueValues.map(val => ({
            value: val,
            label: val,
          }));
          onDetailedColumnDataChange(options);

          // reset selectedCategories when column changes
          onCategoriesChange([]);
        }
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };

    fetchData();
  }, [selectedRange, selectedColumns]);

  useEffect(() => {
    if (
      !selectedCategories.length ||
      !selectedColumns.length ||
      !rawRecordsBar1.length
    ) {
      setBar1Data({ labels: [], datasets: [] });
      return;
    }

    const colKey = selectedColumns[0].value;
    const colorGen = colorGenerator();

    const datasets = selectedCategories.map((cat) => {
      const total = rawRecordsBar1
        .filter((r) => r[colKey] === cat.value)
        .reduce((sum, r) => sum + (r.total_quantity || 0), 0);

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
  }, [selectedCategories, selectedColumns, rawRecordsBar1]);


  const bar1Options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: `Số lượng theo phân loại`,
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Số lượng sản phẩm",
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
    <div className="p-6 min-h-[calc(100vh-50px)] overflow-hidden flex flex-col">
      <h1 className="text-2xl font-bold mb-4">PHÂN TÍCH SỐ LƯỢNG SẢN PHẨM</h1>
      <div className="flex flex-col gap-6">
        <div className="bg-white shadow p-4 rounded-lg h-[680px] w-full">
          <BarChartFilters1
            selectedRange={selectedRange}
            onRangeChange={onRangeChange}
            selectedColumns={selectedColumns}
            onColumnsChange={onColumnsChange}
            selectedCategories={selectedCategories}
            onCategoriesChange={onCategoriesChange}
            columnOptions={columnOptions}
            detailedColumnData={detailedColumnData}
          />

          <div className="mt-6 h-[500px] relative">
            <Bar data={bar1Data} options={bar1Options} />
          </div>
        </div>

      </div>
    </div>
  );
}
