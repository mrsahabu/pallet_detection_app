import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import Modal from "../shared/modal";
import ApiService from "./data-service";

const ConformationPopup = ({
  openConfirmationModal,
  setOpenConfirmationModal,
  removeAllImages,
  images
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
const apiService = new ApiService()
  // eslint-disable-next-line
  const closeModal = () => {
    setIsModalOpen(false);
    setOpenConfirmationModal(false);
  };

  const uploadImages = () => {
    toast.loading("Please wait");
    apiService.uploadImages(images).then((res)=>{
      toast.dismiss();
      toast.success("Upload Successfully!");
      removeAllImages();
      closeModal();

    }).catch((err)=>{
      toast.dismiss();
      toast.error(`Something went wrong ${err}`);
      removeAllImages();
      closeModal();
    })
  };

  useEffect(() => {
    setIsModalOpen(openConfirmationModal);
  }, [openConfirmationModal]);

  return (
    <Modal isOpen={isModalOpen} onClose={closeModal}>
      <h2 className="text-xl font-bold mb-4">Confirmation</h2>
      <p>Are you sure you want to upload these images?</p>

      <div className="flex justify-between">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
          onClick={uploadImages}
        >
          Yes
        </button>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
          onClick={closeModal}
        >
          No
        </button>
      </div>
    </Modal>
  );
};

export default ConformationPopup;
