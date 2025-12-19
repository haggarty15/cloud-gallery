/**
 * Image Card Component
 */
import React from 'react';

const ImageCard = ({ image, onClick }) => {
  return (
    <div
      className="relative group cursor-pointer overflow-hidden rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300"
      onClick={() => onClick(image)}
    >
      <img
        src={image.thumbnail_url || image.image_url}
        alt={image.title || 'Gallery image'}
        className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
        loading="lazy"
      />
      
      <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
          {image.title && (
            <h3 className="text-lg font-semibold mb-1">{image.title}</h3>
          )}
          {image.description && (
            <p className="text-sm line-clamp-2">{image.description}</p>
          )}
          {image.uploader && (
            <p className="text-xs mt-2 opacity-75">
              by {image.uploader.name}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageCard;
