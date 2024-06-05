import React, { useEffect, useState } from "react";
import Webcam from "react-webcam";
import Modal from "./modal";
import { toast } from "react-toastify";

const CaptureImage = ({ openModal, setOpenModal, capturedImages }) => {
  const webcamRef = React.useRef(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

// eslint-disable-next-line
  const closeModal = () => {
    setIsModalOpen(false);
    setOpenModal(false);
  };

  const capture = React.useCallback(() => {

    const imageSrc = webcamRef.current.getScreenshot();
    capturedImages(imageSrc);
    toast.success("Image Uploaded Successfully")
  }, [webcamRef, capturedImages]);

  useEffect(() => {
    setIsModalOpen(openModal);
  }, [openModal]);

  return (
    <Modal isOpen={isModalOpen} onClose={closeModal}>
      <h2 className="text-xl font-bold mb-4">Capture Picture</h2>
      <Webcam
        audio={false}
        height={120}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={"100%"}
      />

      <div className="flex justify-between">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
          onClick={capture}
        >
          Capture photo
        </button>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
          onClick={closeModal}
        >
          Close
        </button>
      </div>
    </Modal>
  );
};

export default CaptureImage;
