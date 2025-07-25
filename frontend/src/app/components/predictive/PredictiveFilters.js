import React, { useId } from "react";
import Select from "react-select";

const PredictiveFilter = ({
  selectedColumn,
  onColumnChange,
  detailedColumnData,
  selectedNum,
  onNumChange,
  numOptions,
}) => {
  const columnSelectId = useId();
  const optionSelectId = useId();

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <div className="w-48">
        <label htmlFor={optionSelectId} className="block text-sm font-medium">
          Top sản phẩm
        </label>
        <Select
          instanceId={optionSelectId}
          inputId={optionSelectId}
          options={numOptions}
          value={selectedNum}
          onChange={(val) => {
            onNumChange(val);
          }}
        />
      </div>

      <div className="flex-1">
        <label htmlFor={columnSelectId} className="block text-sm font-medium">
          Chọn sản phẩm
        </label>
        <Select
          instanceId={columnSelectId}
          inputId={columnSelectId}
          options={detailedColumnData}
          value={selectedColumn}
          onChange={(val) => {
            onColumnChange(val);
          }}
        />
      </div>
    </div>
  );
};

export default PredictiveFilter;
