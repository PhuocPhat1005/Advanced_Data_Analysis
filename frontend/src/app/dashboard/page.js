"use client";

import {
  Bar,
  Pie,
  Line,
} from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, LineElement, PointElement } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, LineElement, PointElement);

export default function DashboardPage() {
  const dummyLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"];
  const dummyData = [12, 19, 3, 5, 2, 3];

  const barData = {
    labels: dummyLabels,
    datasets: [
      {
        label: "Bar Example",
        data: dummyData,
        backgroundColor: "rgba(54, 162, 235, 0.5)",
      },
    ],
  };

  const pieData = {
    labels: ["Red", "Blue", "Yellow"],
    datasets: [
      {
        label: "Pie Example",
        data: [300, 50, 100],
        backgroundColor: ["#f87171", "#60a5fa", "#facc15"],
        borderWidth: 1,
      },
    ],
  };

  const lineData = {
    labels: dummyLabels,
    datasets: [
      {
        label: "Line Example",
        data: dummyData,
        fill: false,
        borderColor: "#10b981",
        tension: 0.4,
      },
    ],
  };

  const histogramData = {
    labels: dummyLabels,
    datasets: [
      {
        label: "Histogram Example",
        data: dummyData,
        backgroundColor: "#6366f1",
      },
    ],
  };

  return (
    <div className="p-6 h-[calc(100vh-48px)] overflow-hidden">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-2 gap-4 h-full">
        <div className="bg-white rounded-xl shadow-xl p-2 flex flex-col">
          <h2 className="text-lg font-semibold text-center mb-1">Bar Chart</h2>
          <div className="flex-1">
            <Bar data={barData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-xl p-2 flex flex-col">
          <h2 className="text-lg font-semibold text-center mb-1">Pie Chart</h2>
          <div className="flex-1">
            <Pie data={pieData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-xl p-2 flex flex-col">
          <h2 className="text-lg font-semibold text-center mb-1">Line Chart</h2>
          <div className="flex-1">
            <Line data={lineData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-xl p-2 flex flex-col">
          <h2 className="text-lg font-semibold text-center mb-1">Histogram</h2>
          <div className="flex-1">
            <Bar data={histogramData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>
      </div>
    </div>
  );
}
