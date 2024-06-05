import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import Modal from "./modal";
import ApiService from "../data-service";
import RadioButton from "../radioButtons";
import ImageDetailsModal from "./imageDetails";

const ConformationPopup = ({
  openConfirmationModal,
  setOpenConfirmationModal,
  removeAllImages,
  images,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState("buy");
  const [openImageDetailModal, setOpenImageDetailModal] = useState(false);
  const [imageDetails, setImageDetails] = useState();
  const apiService = new ApiService();

  const handleChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const onCloseModal = () => {
    setIsModalOpen(false);
    setOpenConfirmationModal(false);
    setOpenImageDetailModal(false);
  };

  const uploadImages = () => {
    toast.loading("Please wait");
    apiService
      .uploadImages(images, selectedOption)
      .then((res) => {
        toast.dismiss();
        toast.success("Upload Successfully!");
        removeAllImages();
        setImageDetails(res.data);
        setOpenImageDetailModal(true);
      })
      .catch((err) => {
        toast.dismiss();
        toast.error(`Something went wrong ${err}`);
        removeAllImages();
        onCloseModal();
      });
  };

  useEffect(() => {
    setIsModalOpen(openConfirmationModal);
  }, [openConfirmationModal]);

  return (
    <Modal isOpen={isModalOpen} onClose={onCloseModal}>
      <h2 className="text-xl font-bold mb-4">Confirmation</h2>

      <div className=" flex items-center justify-center">
        <div className="p-4 bg-white rounded shadow-md">
          <h1 className="text-2xl font-bold mb-4">
            {" "}
            Do you want to sell or buy pallets ?
          </h1>
          <RadioButton
            label="Buy"
            name="options"
            value="buy"
            checked={selectedOption === "buy"}
            onChange={handleChange}
          />
          <RadioButton
            label="Sell"
            name="options"
            value="sell"
            checked={selectedOption === "sell"}
            onChange={handleChange}
          />
        </div>
      </div>
      <ImageDetailsModal
        isOpen={openImageDetailModal}
        onCloseModal={onCloseModal}
        data={imageDetails}
      />

      <p className="mt-4 text-lg font-bold">
        Are you sure you want to upload these images?
      </p>
      <div className="flex justify-between">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
          onClick={uploadImages}
        >
          Yes
        </button>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
          onClick={onCloseModal}
        >
          No
        </button>
      </div>
    </Modal>
  );
};

export default ConformationPopup;
