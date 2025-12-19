/**
 * Admin Dashboard Component
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getPendingImages, approveImage, rejectImage } from '../services/api';

const AdminDashboard = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processing, setProcessing] = useState(null);
  const [rejectionReason, setRejectionReason] = useState('');
  const [showRejectModal, setShowRejectModal] = useState(null);

  const { isAdmin, idToken } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadPendingImages();
  }, [isAdmin, navigate]);

  const loadPendingImages = async () => {
    try {
      setLoading(true);
      const data = await getPendingImages(idToken);
      setImages(data.images);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (imageId) => {
    if (!window.confirm('Are you sure you want to approve this image?')) {
      return;
    }

    try {
      setProcessing(imageId);
      await approveImage(imageId, idToken);
      setImages((prev) => prev.filter((img) => img.id !== imageId));
    } catch (err) {
      alert(`Failed to approve: ${err.message}`);
    } finally {
      setProcessing(null);
    }
  };

  const handleReject = async (imageId) => {
    try {
      setProcessing(imageId);
      await rejectImage(imageId, rejectionReason, idToken);
      setImages((prev) => prev.filter((img) => img.id !== imageId));
      setShowRejectModal(null);
      setRejectionReason('');
    } catch (err) {
      alert(`Failed to reject: ${err.message}`);
    } finally {
      setProcessing(null);
    }
  };

  if (loading) {
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
          <p>Error: {error}</p>
          <button
            onClick={loadPendingImages}
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
      <h1 className="text-4xl font-bold mb-8">Admin Dashboard</h1>

      <div className="mb-4 flex justify-between items-center">
        <h2 className="text-2xl font-semibold">
          Pending Images ({images.length})
        </h2>
        <button
          onClick={loadPendingImages}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Refresh
        </button>
      </div>

      {images.length === 0 ? (
        <div className="text-center text-gray-600 py-12">
          <p className="text-xl">No pending images to review.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {images.map((image) => (
            <div
              key={image.id}
              className="bg-white rounded-lg shadow-md overflow-hidden"
            >
              <img
                src={image.thumbnail_url || image.image_url}
                alt={image.title || 'Pending image'}
                className="w-full h-64 object-cover"
              />

              <div className="p-4">
                {image.title && (
                  <h3 className="text-lg font-semibold mb-2">{image.title}</h3>
                )}

                {image.description && (
                  <p className="text-gray-700 text-sm mb-3 line-clamp-3">
                    {image.description}
                  </p>
                )}

                <div className="text-sm text-gray-600 mb-4">
                  <p>Uploaded by: {image.user_name || image.user_email}</p>
                  <p>
                    Date: {new Date(image.uploaded_at).toLocaleDateString()}
                  </p>
                  {image.metadata && (
                    <p>
                      Size: {image.metadata.width} x {image.metadata.height}
                    </p>
                  )}
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => handleApprove(image.id)}
                    disabled={processing === image.id}
                    className="flex-1 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    {processing === image.id ? 'Processing...' : 'Approve'}
                  </button>

                  <button
                    onClick={() => setShowRejectModal(image.id)}
                    disabled={processing === image.id}
                    className="flex-1 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Reject Modal */}
      {showRejectModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
          onClick={() => setShowRejectModal(null)}
        >
          <div
            className="bg-white rounded-lg p-6 max-w-md w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="text-xl font-bold mb-4">Reject Image</h3>

            <p className="text-gray-600 mb-4">
              Please provide a reason for rejection (optional):
            </p>

            <textarea
              value={rejectionReason}
              onChange={(e) => setRejectionReason(e.target.value)}
              placeholder="e.g., Image does not meet quality standards..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-4"
              rows="4"
            />

            <div className="flex gap-2">
              <button
                onClick={() => handleReject(showRejectModal)}
                disabled={processing === showRejectModal}
                className="flex-1 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:bg-gray-400"
              >
                {processing === showRejectModal ? 'Rejecting...' : 'Reject'}
              </button>
              <button
                onClick={() => {
                  setShowRejectModal(null);
                  setRejectionReason('');
                }}
                className="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
