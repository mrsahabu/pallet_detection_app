import React, { useState } from "react";
import CaptureImage from "../shared/modals/captureImage";
import ConformationPopup from "../shared/modals/confirmModal";
import ImageCarousel from "../shared/modals/imageCarousel";

const UploadCapturePicture = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [openModal, setOpenModal] = useState(false);
  const [openConfirmationModal, setOpenConfirmationModal] = useState(false);
  
  const [images, setImages] = useState([]);

  const handleFileInputChange = (event) => {
    const files = event.target.files;
    if (files.length) {
      setSelectedFile(true);
      const newImages = Array.from(files).map((file) => ({
        file,
        previewUrl: URL.createObjectURL(file),
      }));
      const newIndexedImages = [...images, ...newImages].map((item, index) => ({
        ...item,
        index,
      }));
      setImages([...newIndexedImages]);
    }
  };

  const handleRemoveImage = (image) => {
    const newImages = [...images];
    const index = newImages.findIndex(x=>x.index === image.index)
    newImages.splice(index, 1);
    setImages(newImages);
    if (!newImages.length) {
      setSelectedFile(false);
      window.location.reload()
    }
  };

  const removeAllImages = () => {
    setImages([]);
    setSelectedFile(false);
  };

  const capturedImages = (image) => {
    setSelectedFile(true);
    const newImages = {
      file: image,
      previewUrl: image,
      base64: true,
    };
    const newIndexedImages = [...images, newImages].map((item, index) => ({
      ...item,
      index,
    }));
    setImages([...newIndexedImages]);
  };

  const openCaptureModal = () => {
    setOpenModal(true);
  };
  const openConfirmation = () => {
    setOpenConfirmationModal(true);
  };

  return (
    <div className="min-h-screen flex justify-center items-center ">
      <div className="bg-white rounded-lg p-8 shadow-card">
        <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Upload or Capture Picture
        </h2>
        <div className="flex justify-center items-center mb-8">
          <input
            className="hidden"
            id="fileInput"
            type="file"
            accept="image/png, image/jpeg, image/jpg"
            onChange={handleFileInputChange}
            capture="environment"
            multiple
          />
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mr-2"
            onClick={() => document.getElementById("fileInput").click()}
          >
            Upload
          </button>
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            onClick={openCaptureModal}
          >
            Capture
          </button>
        </div>
        <CaptureImage
          openModal={openModal}
          setOpenModal={setOpenModal}
          capturedImages={capturedImages}
        />
        <ConformationPopup
          openConfirmationModal={openConfirmationModal}
          setOpenConfirmationModal={setOpenConfirmationModal}
          removeAllImages={removeAllImages}
          images={images}
        />
        <ImageCarousel images={images} handleRemoveImage={handleRemoveImage} />
        
        {selectedFile && (
          <div className="text-center">
            <p className="text-lg text-gray-800">{selectedFile.name}</p>
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"
              onClick={openConfirmation}
            >
              Upload Selected Images
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadCapturePicture;
