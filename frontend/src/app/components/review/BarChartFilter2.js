import React, { useId } from "react";
import Select from "react-select";

const BarChartFilters2 = ({
  selectedColumn,
  onColumnChange,
  selectedCategories,
  onCategoriesChange,
  columnOptions,
  dataOptions,
}) => {
  const columnSelectId = useId();
  const categorySelectId = useId();

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <div className="w-48 flex-1">
        <label htmlFor={columnSelectId} className="block text-sm font-medium">
          Column
        </label>
        <Select
          instanceId={columnSelectId}
          inputId={columnSelectId}
          options={columnOptions}
          isMulti={false}
          value={selectedColumn}
          onChange={(val) => {
            onColumnChange(val);
            onCategoriesChange([]);
          }}
        />
      </div>

      <div className="flex-1">
        <label htmlFor={categorySelectId} className="block text-sm font-medium">
          Category
        </label>
        <Select
          instanceId={categorySelectId}
          inputId={categorySelectId}
          options={dataOptions}
          isMulti={true}
          value={selectedCategories}
          onChange={(val) => {
            const limited = val.slice(0, 5);
            onCategoriesChange(limited);
          }}
        />
      </div>
    </div>
  );
};

export default BarChartFilters2;