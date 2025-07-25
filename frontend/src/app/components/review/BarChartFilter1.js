import React, { useId } from "react";
import Select from "react-select";

const BarChartFilters1 = ({
  selectedColumn,
  onColumnChange,
  selectedMethods,
  onMethodChange,
  selectedCategories,
  onCategoriesChange,
  dataOptions,
  columnOptions,
  methodOptions,
}) => {
  const columnSelectId = useId();
  const methodSelectId = useId();
  const categorySelectId = useId();

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <div className="w-48">
        <label htmlFor={columnSelectId} className="block text-sm font-medium">
          Column
        </label>
        <Select
          instanceId={columnSelectId}
          inputId={columnSelectId}
          options={columnOptions}
          value={selectedColumn}
          onChange={(val) => {
            onColumnChange(val)
          }}
        />
      </div>

      <div className="w-48">
        <label htmlFor={methodSelectId} className="block text-sm font-medium">
          Method
        </label>
        <Select
          instanceId={methodSelectId}
          inputId={methodSelectId}
          options={methodOptions}
          value={selectedMethods}
          onChange={(val) => {
            onMethodChange(val);
            onCategoriesChange([]);
          }}
        />
      </div>

      <div className="w-48 flex-1">
        <label htmlFor={categorySelectId} className="block text-sm font-medium">
          Category
        </label>
        <Select
          instanceId={categorySelectId}
          inputId={categorySelectId}
          options={dataOptions}
          isMulti
          value={selectedCategories}
          onChange={(val) => {
            const MAX = 5;
            const limited = val.slice(0, MAX);
            onCategoriesChange(limited || [])
          }}
        />
      </div>

    </div>
  );
};

export default BarChartFilters1;