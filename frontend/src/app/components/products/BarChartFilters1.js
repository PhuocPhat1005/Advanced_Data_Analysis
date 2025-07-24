import React, { useId } from "react";
import DatePicker from "react-datepicker";
import Select, { components } from "react-select";

// Custom Option with checkbox
const CheckboxOption = (props) => {
  return (
    <components.Option {...props}>
      <input
        type="checkbox"
        checked={props.isSelected}
        onChange={() => {}}
        className="mr-2"
      />
      <label>{props.label}</label>
    </components.Option>
  );
};

const BarChartFiltersV2 = ({
  selectedRange,
  onRangeChange,
  selectedColumns,
  onColumnsChange,
  selectedCategories,
  onCategoriesChange,
  columnOptions,
  detailedColumnData
}) => {
  const columnsSelectId = useId();
  const categoriesSelectId = useId();

  return (
    <div className="flex flex-wrap gap-4 items-center">
      {/* Date range picker */}
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

      {/* Multi-select with checkboxes */}
      <div className="w-80">
        <label htmlFor={columnsSelectId} className="block text-sm font-medium">
          Select Columns
        </label>
        <Select
          instanceId={columnsSelectId}
          inputId={columnsSelectId}
          isMulti
          closeMenuOnSelect={false}
          hideSelectedOptions={false}
          options={columnOptions}
          value={selectedColumns}
          onChange={(val) => onColumnsChange(val || [])}
          components={{ Option: CheckboxOption }}
        />
      </div>

      {/* Keep existing last select */}
      <div className="flex-1">
        <label htmlFor={categoriesSelectId} className="block text-sm font-medium">
          Data
        </label>
        <Select
          instanceId={categoriesSelectId}
          inputId={categoriesSelectId}
          isMulti
          options={
            Array.isArray(detailedColumnData) ? detailedColumnData : []
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

export default BarChartFiltersV2;
