"use client";


import { useEffect, useState } from "react";
import PredictiveFilter from "../components/predictive/PredictiveFilters";



export default function RecommendationPage() {
  const [selectedColumn, onColumnChange] = useState();
  const [detailedColumnData, onDetailedColumnDataChange] = useState();
  const [selectedNum, onNumChange] = useState([]);
  const [recommendedProducts, setRecommendedProducts] = useState([]);

  const numOptions = [
    { value: 3, label: "3" },
    { value: 5, label: "5" },
    { value: 10, label: "10" },
    { value: 15, label: "15" },
  ]

  useEffect(() => {
    const fetchProductNames = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/analysis/predictive/product-names");
        if (!res.ok) {
          throw new Error("Failed to fetch product names");
        }

        const data = await res.json();

        const options = data.name_product.map((item) => ({
          value: item,
          label: item,
        }));

        onDetailedColumnDataChange(options.slice(0, 100));
      } catch (error) {
        console.error("Error fetching product names:", error);
      }
    };

    fetchProductNames();
  }, []);

  useEffect(() => {
    const fetchRecommendedProducts = async () => {
      if (!selectedColumn || !selectedNum) {
        return;
      }
      
      try {
        const res = await fetch("http://127.0.0.1:8000/analysis/predictive/recommend", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name_product: selectedColumn.value,
            topk: Number(selectedNum.value),
          }),
        });

        if (!res.ok) {
          throw new Error("Lỗi khi gọi API gợi ý sản phẩm");
        }
        
        const data = await res.json();

        console.log("Sản phẩm được gợi ý:", data);
        setRecommendedProducts(data);
      } catch (error) {
        console.error("Lỗi khi fetch gợi ý sản phẩm:", error);
      }
    };

    fetchRecommendedProducts();
  }, [selectedNum, selectedColumn]);



  return (
    <div className="p-6 min-h-[calc(100vh-50px)]  overflow-hidden flex flex-col">
      <h1 className="text-2xl font-bold mb-4">GỢI Ý SẢN PHẨM</h1>
      <div className="bg-white shadow p-4 rounded-lg h-[610px] w-full">
        <PredictiveFilter
          selectedColumn={selectedColumn}
          onColumnChange={onColumnChange}
          detailedColumnData={detailedColumnData}
          selectedNum={selectedNum}
          onNumChange={onNumChange}
          numOptions={numOptions}
        />

        <div className="mt-4">
          <h2 className="text-lg font-semibold mb-2">Sản phẩm được gợi ý:</h2>
          <ul className="list-disc pl-6 space-y-1 max-h-[300px] overflow-y-auto">
            {recommendedProducts.map((item, index) => (
              <li key={index}>
                <span className="font-medium">{item.name_dst}</span>
                <span className="text-gray-500 text-sm"> — Danh mục: {item.category_dst}</span>
                <span className="text-gray-500 text-sm"> — Hãng sảng xuất:  {item.brand_dst}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>

        </div>
      </div>

    </div>
  );
}