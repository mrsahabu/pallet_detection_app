import React, { useEffect, useState } from "react";
import Modal from "./modal";
import { Carousel } from "primereact/carousel";

const UserImagesModal = ({ openModal, setOpenModal, images }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [userImages, setUserImages] = useState(images);
  // eslint-disable-next-line
  const closeModal = () => {
    setIsModalOpen(false);
    setOpenModal(false);
  };

  useEffect(() => {
    if (openModal) {
      setIsModalOpen(openModal);
      setUserImages(images);
    }
  }, [openModal, images]);

  const responsiveOptions = [
    {
      breakpoint: "1400px",
      numVisible: 1,
      numScroll: 1,
    },
    {
      breakpoint: "1199px",
      numVisible: 1,
      numScroll: 1,
    },
    {
      breakpoint: "767px",
      numVisible: 1,
      numScroll: 1,
    },
    {
      breakpoint: "575px",
      numVisible: 1,
      numScroll: 1,
    },
  ];

  const imageTemplate = (image) => {
    return (
      <div className="w-full p-2 shadow-2xl">
        <div className="relative">
          <img
            src={image.img_path}
            alt={`userImages`}
            className="w-full h-48 object-contain rounded-lg"
          />
        </div>
      </div>
    );
  };

  return (
    <Modal isOpen={isModalOpen} onClose={closeModal} showcloseButton={true}>
      <h2 className="text-xl font-bold mb-4">User Uploaded Images</h2>
      <div className="container mx-auto px-4 py-8">
      {userImages && userImages.length > 0 && (
        <div className="card">
          <Carousel
            value={userImages}
            numVisible={3}
            numScroll={3}
            responsiveOptions={responsiveOptions}
            className="custom-carousel"
            circular
            itemTemplate={imageTemplate}
          />
        </div>
      )}
    </div>
    </Modal>
  );
};

export default UserImagesModal;
