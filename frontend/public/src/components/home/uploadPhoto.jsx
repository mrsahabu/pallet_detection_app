import React, { useState } from "react";
import CaptureImage from "../shared/captureImage";
import ConformationPopup from "../shared/confirmModal";

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
      setImages((prevImages) => [...prevImages, ...newImages]);
    }
  };

  const handleRemoveImage = (index) => {
    const newImages = [...images];
    newImages.splice(index, 1);
    setImages(newImages);
    if (!newImages.length) {
      setSelectedFile(false);
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
    setImages((prevImages) => [...prevImages, newImages]);
  };

  const openCaptureModal = () => {
    setOpenModal(true);
  };
  const openConfirmation = () => {
    setOpenConfirmationModal(true);
  };

  return (
    <div className="bg-gradient-to-br from-purple-500 to-indigo-500 min-h-screen flex justify-center items-center">
      <div className="bg-white rounded-lg p-8 shadow-md">
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
        <div className="flex flex-wrap -mx-2">
          {images.map((image, index) => (
            <div
              key={index}
              className="w-full sm:w-1/2 md:w-1/3 lg:w-2/4 xl:w-2/6 p-2"
            >
              <div className="relative">
                <img
                  src={image.previewUrl}
                  alt={`userImage${index + 1}`}
                  className="w-full h-48 object-contain rounded-lg"
                />
                <button
                  className="absolute top-0 right-0 p-2 bg-white rounded-full shadow-md hover:bg-gray-100"
                  onClick={() => handleRemoveImage(index)}
                >
                  <svg
                    className="h-6 w-6 text-red-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
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
