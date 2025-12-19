/**
 * Gallery Component - Main public gallery view
 */
import React, { useState, useEffect } from 'react';
import { getGallery } from '../services/api';
import ImageCard from './ImageCard';
import ImageModal from './ImageModal';

const Gallery = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    loadImages();
  }, [page]);

  const loadImages = async () => {
    try {
      setLoading(true);
      const data = await getGallery(page, 20);
      
      if (page === 1) {
        setImages(data.images);
      } else {
        setImages((prev) => [...prev, ...data.images]);
      }
      
      setHasMore(data.pagination.page < data.pagination.pages);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleImageClick = (image) => {
    setSelectedImage(image);
  };

  const handleCloseModal = () => {
    setSelectedImage(null);
  };

  const handleLoadMore = () => {
    setPage((prev) => prev + 1);
  };

  if (loading && page === 1) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>Error loading gallery: {error}</p>
          <button
            onClick={() => loadImages()}
            className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8 text-center">Gallery</h1>

      {images.length === 0 ? (
        <div className="text-center text-gray-600">
          <p className="text-xl">No images in the gallery yet.</p>
          <p className="mt-2">Check back soon!</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {images.map((image) => (
              <ImageCard
                key={image.id}
                image={image}
                onClick={handleImageClick}
              />
            ))}
          </div>

          {hasMore && (
            <div className="flex justify-center mt-8">
              <button
                onClick={handleLoadMore}
                disabled={loading}
                className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? 'Loading...' : 'Load More'}
              </button>
            </div>
          )}
        </>
      )}

      {selectedImage && (
        <ImageModal image={selectedImage} onClose={handleCloseModal} />
      )}
    </div>
  );
};

export default Gallery;
