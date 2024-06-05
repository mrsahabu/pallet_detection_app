
import React from 'react';

const RadioButton = ({ label, name, value, checked, onChange }) => {
  return (
    <label className="inline-flex items-center mt-3 mx-3">
      <input
        type="radio"
        className="form-radio h-5 w-5 text-blue-600"
        name={name}
        value={value}
        checked={checked}
        onChange={onChange}
      />
      <span className="ml-2 text-gray-700">{label}</span>
    </label>
  );
};

export default RadioButton;
