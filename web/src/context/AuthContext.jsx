/**
 * Authentication Context Provider
 */
import React, { createContext, useState, useEffect, useContext } from 'react';
import {
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  createUserWithEmailAndPassword,
} from 'firebase/auth';
import { auth, googleProvider } from '../services/firebase';

const AuthContext = createContext({});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [idToken, setIdToken] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      setCurrentUser(user);
      
      if (user) {
        try {
          const token = await user.getIdToken();
          setIdToken(token);
          
          // Check if user is admin
          const tokenResult = await user.getIdTokenResult();
          setIsAdmin(!!tokenResult.claims.admin);
        } catch (error) {
          console.error('Error getting token:', error);
        }
      } else {
        setIdToken(null);
        setIsAdmin(false);
      }
      
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const signup = async (email, password) => {
    return createUserWithEmailAndPassword(auth, email, password);
  };

  const login = async (email, password) => {
    return signInWithEmailAndPassword(auth, email, password);
  };

  const loginWithGoogle = async () => {
    return signInWithPopup(auth, googleProvider);
  };

  const logout = async () => {
    setIdToken(null);
    setIsAdmin(false);
    return signOut(auth);
  };

  const refreshToken = async () => {
    if (currentUser) {
      const token = await currentUser.getIdToken(true);
      setIdToken(token);
      return token;
    }
    return null;
  };

  const value = {
    currentUser,
    idToken,
    isAdmin,
    loading,
    signup,
    login,
    loginWithGoogle,
    logout,
    refreshToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
