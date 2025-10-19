import { useState, useEffect, useCallback, useRef } from "react";
import { jwtDecode } from "jwt-decode"; // install with: npm install jwt-decode

const TOKEN_KEY = "authToken";

// Helper function to validate token structure and expiry
const isValidToken = (token) => {
  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000; // Convert to seconds
    
    // Check if token has required fields
    if (!decoded.exp || !decoded.sub) {
      return false;
    }
    
    // Check if token is expired
    if (decoded.exp < currentTime) {
      return false;
    }
    
    return true;
  } catch (err) {
    return false;
  }
};

export default function useAuth() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const logoutRef = useRef();

  // Logout: clear everything
  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setUser(null);
  }, []);

  // Store logout in ref to avoid dependency issues
  logoutRef.current = logout;

  // Load user from localStorage on first render
  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token && isValidToken(token)) {
      try {
        const decoded = jwtDecode(token);
        setUser(decoded);
      } catch (err) {
        console.error("Failed to decode valid token:", err);
        localStorage.removeItem(TOKEN_KEY);
      }
    } else if (token) {
      // Token exists but is invalid, remove it
      localStorage.removeItem(TOKEN_KEY);
    }
    setIsLoading(false);
  }, []);

  // Set up interval to check token expiry
  useEffect(() => {
    if (!user) return;

    const checkTokenExpiry = () => {
      const token = localStorage.getItem(TOKEN_KEY);
      if (token && !isValidToken(token)) {
        logoutRef.current();
      }
    };

    // Check every minute
    const interval = setInterval(checkTokenExpiry, 60000);
    
    return () => clearInterval(interval);
  }, [user]);

  // Login: save token + set user
  const login = useCallback((token) => {
    if (!token || typeof token !== 'string') {
      throw new Error('Invalid token provided');
    }

    if (!isValidToken(token)) {
      throw new Error('Token is invalid or expired');
    }

    try {
      const decoded = jwtDecode(token);
      localStorage.setItem(TOKEN_KEY, token);
      setUser(decoded);
    } catch (err) {
      console.error("Failed to decode token:", err);
      throw new Error('Failed to process authentication token');
    }
  }, []);

  // Check auth state
  const isAuthenticated = !!user;

  return { user, isAuthenticated, login, logout, isLoading };
}
