"use client";

import {
  Chart as ChartJS,
  TimeScale,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import "chartjs-adapter-date-fns";
import { Bar, Line } from "react-chartjs-2";
import { useEffect, useState } from "react";
import "react-datepicker/dist/react-datepicker.css";
import LineChartFilters from "../components/revenue/LineChartFilters";
import BarChartFilters from "../components/revenue/BarChartFilters";
import { colorGenerator } from "../utils/getColor";


ChartJS.register(
  CategoryScale,
  TimeScale,
  LinearScale,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
  Title
);




export default function DashboardPage() {
  // Line chart
  const [selectedDate, onDateChange] = useState(new Date('2016-01-01'));
  const [selectedColumnLine, setSelectedColumnLine] = useState(null);
  const [detailedColumnData, onDetailedColumnDataChange] = useState([]);
  const [selectedCategoriesLine, setSelectedCategoriesLine] = useState([]);
  const [selectedMode, setSelectedMode] = useState({ value: "Y", label: "By Year" });
  const [lineData, setLineData] = useState({ labels: [], datasets: [] });
  const [rawLineRecords, setRawLineRecords] = useState([]);

  // Bar chart
  const [selectedRange, setSelectedRange] = useState([new Date('2016-01-01'), null]);
  const [selectedColumnBar, setSelectedColumnBar] = useState(null);
  const [categoryOptionsBar, setCategoryOptionsBar] = useState([]);
  const [selectedCategoriesBar, setSelectedCategoriesBar] = useState([]);
  const [barData, setBarData] = useState({ labels: [], datasets: [] });
  const [rawBarRecords, setRawBarRecords] = useState([]);

  const dataOptions = [
    { value: "product_source", label: "Product Source" },
    { value: "category", label: "Category" },
    { value: "current_seller", label: "Current Seller" },
  ];




  // Line fetch
  useEffect(() => {
    const fetchRawData = async () => {
      if (!selectedColumnLine || !selectedMode) return;

      try {
        const res = await fetch(
          `http://127.0.0.1:8000/analysis/descriptive/revenue/timeline?categorized_column=${selectedColumnLine.value}&time_mode=${selectedMode.value}`
        );
        const json = await res.json();
        if (Array.isArray(json.records)) {
          setRawLineRecords(json.records);

          // Cập nhật filter options
          const uniqueCats = [...new Set(json.records.map(r => r[selectedColumnLine.value]))];
          onDetailedColumnDataChange(uniqueCats.map(val => ({ value: val, label: val })));
        }
      } catch (err) {
        console.error("Fetch failed:", err);
      }
    };

    fetchRawData();
  }, [selectedColumnLine, selectedMode]);

  // Line filter
  useEffect(() => {
    if (!selectedColumnLine || !selectedDate) return;

    const selectedDateStr = selectedDate.toISOString().slice(0, 10);
    console.log("Raw records:", rawLineRecords);

    const filteredByDate = rawLineRecords.filter(r => {
      const ts = r.time_group;
      return ts && ts.slice(0, 10) >= selectedDateStr;
    });

    const filteredByCategory = selectedCategoriesLine.length
      ? filteredByDate.filter(r =>
        selectedCategoriesLine.some(c => c.value === r[selectedColumnLine.value])
      )
      : filteredByDate;

    const getLabel = r => r.time_group?.slice(0, 10);
    const allLabels = [...new Set(filteredByCategory.map(getLabel))].filter(Boolean).sort();
    const categories = [...new Set(filteredByCategory.map(r => r[selectedColumnLine.value]))].slice(0, 5);
    const lineColorGen = colorGenerator();
      
    const datasets = categories.map(cat => {
      const data = allLabels.map(label =>
        filteredByCategory
          .filter(r => getLabel(r) === label && r[selectedColumnLine.value] === cat)
          .reduce((sum, r) => sum + (r.total_revenue || 0), 0)
      );
      
      return {
        label: cat,
        data,
        borderColor: lineColorGen.next().value,
        // backgroundColor: lineColorGen.next().value,
        fill: false,
      };
    });

    setLineData({ labels: allLabels, datasets });
  }, [rawLineRecords, selectedDate, selectedCategoriesLine, selectedColumnLine]);


  // Bar fetch
  useEffect(() => {
    const fetchRawData = async () => {
      if (!selectedColumnBar || !selectedRange?.[0] || !selectedRange?.[1]) {
        console.log("Dữ liệu thiếu:", { selectedColumnBar, selectedRange });
        return;
      }

      const minDate = selectedRange[0].toISOString().slice(0, 10);
      const maxDate = selectedRange[1].toISOString().slice(0, 10);
      const key = selectedColumnBar.value;



      const url = `http://127.0.0.1:8000/analysis/descriptive/revenue/total?categorized_column=${key}&min_date=${minDate}&max_date=${maxDate}`;

      try {
        const res = await fetch(url);
        const json = await res.json();
        console.log("Fetched data:", json);

        if (json.records && Array.isArray(json.records)) {
          setRawBarRecords(json.records);
          const uniqueCategories = Array.from(new Set(json.records.map(r => r[key])));
          const filteredCategories = uniqueCategories.filter(v => v !== undefined && v !== null);
          const options = filteredCategories.map(val => ({ value: val, label: val }));
          console.log("Options:", options);

          setCategoryOptionsBar(options);
        }
      } catch (err) {
        console.error("Fetch error:", err);
      }
    };

    fetchRawData();
  }, [selectedColumnBar, selectedRange]);

  // Bar filter 
  useEffect(() => {
    if (!selectedColumnBar || !selectedRange?.[0] || !selectedRange?.[1]) return;
    if (!selectedCategoriesBar.length) return;
    
    const barColorGen = colorGenerator();
    const key = selectedColumnBar.value;

    const datasets = selectedCategoriesBar.map(cat => {
      const total = rawBarRecords
        .filter(r => r[key] === cat.value)
        .reduce((sum, r) => sum + (r.total_revenue || 0), 0);

      return {
        label: cat.label,
        data: [total],
        backgroundColor: barColorGen.next().value,
      };
    });

    setBarData({
      labels: [''],
      datasets,
    });
  }, [rawBarRecords, selectedCategoriesBar, selectedColumnBar, selectedRange]);



  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      title: {
        display: true,
        text: 'Doanh thu theo thời gian và phân loại',
      },
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'month',
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: `Doanh thu theo phân loại`,
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Doanh thu",
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
      <h1 className="text-2xl font-bold mb-4">PHÂN TÍCH DOANH THU</h1>
      <div className="flex flex-col gap-6 ">
        {/* Line Chart Section */}
        <div className="bg-white shadow p-4 rounded-lg h-[610px] w-full">
          <LineChartFilters
            selectedDate={selectedDate}
            onDateChange={onDateChange}
            selectedColumn={selectedColumnLine}
            onColumnChange={setSelectedColumnLine}
            selectedCategories={selectedCategoriesLine}
            onCategoriesChange={setSelectedCategoriesLine}
            dataOptions={dataOptions}
            detailedColumnData={detailedColumnData}
            selectedMode={selectedMode}
            onModeChange={setSelectedMode}
          />

          <div className="mt-6 h-[500px] relative">
            <Line data={lineData} options={lineOptions} />
          </div>
        </div>

        {/* Bar Chart Section */}
        <div className="bg-white shadow p-4 rounded-lg h-[610px] w-full">
          <BarChartFilters
            selectedRange={selectedRange}
            onRangeChange={setSelectedRange}
            selectedColumn={selectedColumnBar}
            onColumnChange={setSelectedColumnBar}
            selectedCategories={selectedCategoriesBar}
            onCategoriesChange={setSelectedCategoriesBar}
            dataOptions={dataOptions}
            detailedColumnData={categoryOptionsBar}
          />
          <div className="mt-6 h-[500px] relative">
            <Bar data={barData} options={barOptions} />
          </div>
        </div>
      </div>
    </div>
  );
}