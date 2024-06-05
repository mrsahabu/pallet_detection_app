import React, { useEffect, useState } from "react";
import { Carousel } from "primereact/carousel";

const ImageCarousel = ({ images, handleRemoveImage }) => {
  const [imageList, setImageList] = useState(images);

  useEffect(() => {
    if (images.length > 0) {
      setImageList(images);
    } else {
      setImageList([]);
    }
  }, [images]);

  const removeImages = (image) => {
    const newImages = [...images];
    const index = newImages.findIndex(x=>x.index === image.index)
    newImages.splice(index, 1);
    setImageList(newImages);
    handleRemoveImage(image);
  };

  const responsiveOptions = [
    {
      breakpoint: "1400px",
      numVisible: 3,
      numScroll: 1,
    },
    {
      breakpoint: "1199px",
      numVisible: 3,
      numScroll: 1,
    },
    {
      breakpoint: "767px",
      numVisible: 2,
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
            src={image.previewUrl}
            alt={`userImages`}
            className="w-full h-48 object-contain rounded-lg"
          />
          <button
            className="absolute top-0 right-0 p-2 bg-white rounded-full shadow-md hover:bg-gray-100"
            onClick={() => removeImages(image)}
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
    );
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {imageList && imageList.length > 0 && (
        <div className="card">
          <Carousel
            value={imageList}
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
  );
};

export default ImageCarousel;
