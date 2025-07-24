import React, { useId } from "react";
import DatePicker from "react-datepicker";
import Select from "react-select";

const LineChartFilters = ({
  selectedDate, // date filter
  onDateChange,
  selectedColumn, // column filter
  onColumnChange,
  selectedCategories, // pattern data from column filter
  onCategoriesChange,
  dataOptions, // data options for column (pre declared, not based on users input or queries)
  detailedColumnData,
  selectedMode,
  onModeChange
}) => {
  const columnSelectId = useId();
  const categoriesSelectId = useId();
  const modeSelectId = useId();

  const modeOptions = [
    { value: "D", label: "By Day" },
    { value: "M", label: "By Month" },
    { value: "Y", label: "By Year" },
  ];

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <div>
        <label className="block text-sm font-medium">Date</label>
        <DatePicker
          selected={selectedDate}
          onChange={(date) => date && onDateChange(date)}
          dateFormat="yyyy-MM-dd"
          showMonthDropdown
          showYearDropdown
          dropdownMode="select"
          className="border px-2 py-1 rounded"
        />
      </div>

      <div className="w-48">
        <label htmlFor={columnSelectId} className="block text-sm font-medium">
          Columns
        </label>
        <Select
          instanceId={columnSelectId}
          inputId={columnSelectId}
          options={dataOptions}
          value={selectedColumn}
          onChange={(val) => {
            onColumnChange(val);
            onCategoriesChange([]);
          }}
        />
      </div>

      <div className="w-40">
        <label htmlFor={modeSelectId} className="block text-sm font-medium">
          Mode
        </label>
        <Select
          instanceId={modeSelectId}
          inputId={modeSelectId}
          options={modeOptions}
          value={selectedMode}
          onChange={(val) => onModeChange(val)}
        />
      </div>

      <div className="flex-1">
        <label htmlFor={categoriesSelectId} className="block text-sm font-medium">
          Data
        </label>
        <Select
          instanceId={categoriesSelectId}
          inputId={categoriesSelectId}
          isMulti
          options={
            selectedColumn && Array.isArray(detailedColumnData)
              ? detailedColumnData
              : []
          }
          value={selectedCategories}
          onChange={(val) => {
            const MAX = 5;
            const limited = val.slice(0, MAX);
            onCategoriesChange(limited || []);
          }}
        />

      </div>
    </div>
  );
};

export default LineChartFilters;