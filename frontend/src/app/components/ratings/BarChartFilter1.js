import React, { useId } from "react";
import DatePicker from "react-datepicker";
import Select from "react-select";

const BarChartFilters1 = ({
  selectedColumn,
  onColumnChange,
  dataOptions,
  selectedMethods,
  onMethodChange,
  methodOptions,
}) => {
  const columnSelectId = useId();
  const methodId = useId();

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <div className="w-48">
        <label htmlFor={columnSelectId} className="block text-sm font-medium">
          Column
        </label>
        <Select
          instanceId={columnSelectId}
          inputId={columnSelectId}
          options={dataOptions}
          value={selectedColumn}
          onChange={(val) => {onColumnChange(val)}}
        />
      </div>
      
      <div className="w-48">
        <label htmlFor={methodId} className="block text-sm font-medium">
          Method
        </label>
        <Select
          instanceId={methodId}
          inputId={methodId}
          options={methodOptions}
          value={selectedMethods}
          onChange={(val) => {onMethodChange(val)}}
        />
      </div>
    </div>
  );
};

export default BarChartFilters1;