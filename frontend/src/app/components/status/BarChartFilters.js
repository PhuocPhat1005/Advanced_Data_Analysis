import React, { useId } from "react";
import DatePicker from "react-datepicker";
import Select from "react-select";

const BarChartFilters = ({
  selectedRange,
  onRangeChange,
  selectedColumn,
  onColumnChange,
  selectedCategories,
  onCategoriesChange,
  dataOptions,
  detailedColumnData,
  selectedOptions,
  onOptionsChange,
  options,
}) => {
  const columnSelectId = useId();
  const categoriesSelectId = useId();
  const statusSelectedId = useId();

  return (
    <div className="flex flex-wrap gap-4 items-center">

      {/* Date range input */}
      <div>
        <label className="block text-sm font-medium">Date Range</label>
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
          className="border px-2 py-1 rounded"
        />
      </div>
      {/* Column */}
      <div className="w-48">
        <label htmlFor={columnSelectId} className="block text-sm font-medium">
          Column
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

      {/* Status: 0 hoac 1 */}
      <div className="w-74">
        <label htmlFor={statusSelectedId} className="block text-sm font-medium">
          Status
        </label>
        <Select
          instanceId={statusSelectedId}
          inputId={statusSelectedId}
          options={options}
          isMulti
          value={selectedOptions}
          onChange={(val) => {
            onOptionsChange(val);
          }}
        />
      </div>
      {/* Categories */}
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

export default BarChartFilters;
