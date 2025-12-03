// frontend/src/pages/Register.jsx
import React, { useState } from "react";

const Register = ({ setLoggedIn }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    if (!isValidEmail(email)) {
      setError("Please enter a valid email address (e.g., user@example.com)");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ full_name: name, email, password }),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data?.detail || "Registration failed");
        return;
      }
      localStorage.setItem("userEmail", email);
      const userName = data?.user?.name || email.split("@")[0];
      localStorage.setItem("userName", userName);
      alert("Registration successful! Please login.");
      window.location.hash = "#/login";
    } catch (error) {
      setError("Network error. Please check your connection.");
      console.error("An error occurred during registration:", error);
    }
  };

  return (
    <div className="relative min-h-screen bg-linear-to-br from-blue-50 via-purple-50 to-pink-50 overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img
          src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1920&q=80"
          alt="Career Success"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-linear-to-br from-blue-900/80 via-purple-900/70 to-pink-900/80"></div>
        <div className="absolute inset-0 bg-linear-to-t from-black/40 to-transparent"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-4 py-16">
        <div className="relative bg-white/90 backdrop-blur-md border border-gray-200 p-8 rounded-2xl shadow-2xl w-full max-w-md transform transition-all duration-300 hover:scale-[1.02] hover:shadow-blue-500/30">
          <h2 className="text-3xl font-bold text-center bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Create Account
          </h2>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Full Name
              </label>
              <input
                id="name"
                type="text"
                className="w-full p-3 rounded-lg bg-white border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                placeholder="John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                className="w-full p-3 rounded-lg bg-white border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                className="w-full p-3 rounded-lg bg-white border border-gray-300 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                placeholder="********"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 rounded-lg bg-linear-to-r from-blue-600 to-purple-600 text-white font-semibold hover:shadow-lg transition"
            >
              Register
            </button>
          </form>

          <p className="text-center text-sm text-gray-600 mt-4">
            Already have an account?{" "}
            <a
              href="#/login"
              className="text-blue-600 hover:text-blue-700 font-semibold"
            >
              Login
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
