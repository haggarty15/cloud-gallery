/**
 * Header Component
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const { currentUser, isAdmin, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <header className="bg-white shadow-md">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-gray-800">
            Cloud Gallery
          </Link>

          <div className="flex items-center space-x-4">
            <Link to="/" className="text-gray-600 hover:text-gray-800">
              Gallery
            </Link>

            {currentUser ? (
              <>
                {isAdmin && (
                  <Link
                    to="/admin"
                    className="text-blue-600 hover:text-blue-800 font-semibold"
                  >
                    Admin Dashboard
                  </Link>
                )}
                <span className="text-gray-600">
                  {currentUser.email}
                </span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                to="/login"
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Login
              </Link>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
