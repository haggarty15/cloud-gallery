/**
 * Main App Component
 */
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Header from './components/Header';
import Gallery from './components/Gallery';
import Login from './components/Login';
import AdminDashboard from './components/AdminDashboard';

function App() {
  const { isAdmin } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Routes>
        <Route path="/" element={<Gallery />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/admin"
          element={isAdmin ? <AdminDashboard /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  );
}

export default App;
