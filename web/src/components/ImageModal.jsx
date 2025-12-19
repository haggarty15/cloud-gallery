/**
 * Image Modal Component
 */
import React, { useEffect } from 'react';

const ImageModal = ({ image, onClose }) => {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [onClose]);

  if (!image) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4"
      onClick={onClose}
    >
      <div
        className="relative max-w-7xl max-h-full"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute -top-12 right-0 text-white text-4xl hover:text-gray-300 z-10"
          aria-label="Close modal"
        >
          &times;
        </button>

        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <img
              src={image.image_url}
              alt={image.title || 'Full size image'}
              className="max-w-full max-h-[80vh] object-contain rounded-lg"
            />
          </div>

          {(image.title || image.description || image.uploader) && (
            <div className="md:w-80 bg-white rounded-lg p-6 max-h-[80vh] overflow-y-auto">
              {image.title && (
                <h2 className="text-2xl font-bold mb-4">{image.title}</h2>
              )}

              {image.description && (
                <p className="text-gray-700 mb-4 whitespace-pre-wrap">
                  {image.description}
                </p>
              )}

              {image.uploader && (
                <div className="border-t pt-4">
                  <p className="text-sm text-gray-600">Uploaded by</p>
                  <p className="font-semibold">{image.uploader.name}</p>
                </div>
              )}

              {image.uploaded_at && (
                <div className="mt-4">
                  <p className="text-sm text-gray-600">Uploaded on</p>
                  <p className="text-sm">
                    {new Date(image.uploaded_at).toLocaleDateString()}
                  </p>
                </div>
              )}

              {image.metadata && (
                <div className="mt-4 text-xs text-gray-500">
                  <p>
                    Dimensions: {image.metadata.width} x {image.metadata.height}
                  </p>
                  {image.metadata.file_size && (
                    <p>
                      Size: {(image.metadata.file_size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageModal;
