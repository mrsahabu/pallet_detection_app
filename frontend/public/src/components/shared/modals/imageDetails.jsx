// Modal.js
import React from "react";

const ImageDetailsModal = ({ isOpen, onCloseModal, data }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
      <div className="bg-white rounded-lg shadow-lg w-1/2">
        <div className="flex justify-between items-center border-b p-4">
          <h2 className="text-xl font-bold">Record Details</h2>
          <button
            onClick={onCloseModal}
            className="text-gray-600 text-2xl hover:text-gray-800"
          >
            &times;
          </button>
        </div>
        <div className="p-4">
          <div className="mb-2 capitalize">
            <strong>Buy or Sell:</strong> {data.buy_or_sell}
          </div>
          <div className="mb-2">
            <strong>CO2 FC:</strong> {data.co2_fc}
          </div>
          <div className="mb-2">
            <strong>CO2 Saving Count:</strong> {data.co2_saving_count}
          </div>
          <div className="mb-2">
            <strong>Pallets Count:</strong> {data.pallets_count}
          </div>
          <div className="mb-2">
            <strong>Price per Piece:</strong> {data.price_piece}
          </div>
          <div className="mb-2">
            <strong>Total Price:</strong> {data.total_price}
          </div>
          <div className="mb-2">
            <strong>Total Transport:</strong> {data.total_transport}
          </div>
          <div className="mb-2">
            <strong>Transport Cost:</strong> {data.transport_cost}
          </div>
          <div className="mb-2">
            <strong>Transport FC Count:</strong> {data.transport_fc_count}
          </div>
        </div>
        <div className="border-t p-4 flex justify-end">
          <button
            onClick={onCloseModal}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageDetailsModal;
