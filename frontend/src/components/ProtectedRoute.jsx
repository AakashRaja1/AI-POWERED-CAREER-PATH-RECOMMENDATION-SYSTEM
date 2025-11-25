import React, { useEffect } from "react";

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      // Redirect to login if not authenticated
      window.location.hash = "#/login";
    }
  }, [token]);

  // Show children only if authenticated
  if (!token) {
    return (
      <div className="min-h-screen bg-neutral-900 text-gray-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl mb-4 text-blue-400">🔒 Authentication Required</p>
          <p className="text-gray-400 mb-4">Please register and login to access this page</p>
          <div className="flex gap-4 justify-center">
            <a
              href="#/register"
              className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg transition-all"
            >
              Register
            </a>
            <a
              href="#/login"
              className="inline-block bg-neutral-700 hover:bg-neutral-600 text-white font-semibold py-2 px-6 rounded-lg transition-all"
            >
              Login
            </a>
          </div>
        </div>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;

