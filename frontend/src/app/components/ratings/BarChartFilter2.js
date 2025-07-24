import React, { useId } from "react";
import DatePicker from "react-datepicker";
import Select from "react-select";

const BarChartFilters2 = ({
  selectedColumn,
  onColumnChange,
  selectedCategories,
  onCategoriesChange,
  dataOptions,
}) => {
  const columnSelectId = useId();
  const categorySelectId = useId();

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <div className="flex-1">
        <label htmlFor={columnSelectId} className="block text-sm font-medium">
          Column
        </label>
        <Select
          instanceId={columnSelectId}
          inputId={columnSelectId}
          options={dataOptions}
          value={selectedColumn}
          onChange={(val) => {
            onColumnChange(val)

          }}
        />
      </div>

      <div className="w-48">
        <label htmlFor={categorySelectId} className="block text-sm font-medium">
          Category
        </label>
        <Select
          instanceId={categorySelectId}
          inputId={categorySelectId}
          options={dataOptions}
          value={selectedCategories}
          onChange={(val) => { onCategoriesChange(val) }}
        />
      </div>
    </div>
  );
};

export default BarChartFilters2;