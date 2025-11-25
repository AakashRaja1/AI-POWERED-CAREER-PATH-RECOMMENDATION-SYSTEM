// frontend/src/pages/Register.jsx
import React, { useState } from "react";

const Register = ({ setLoggedIn }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ full_name: name, email, password }),
      });
      if (response.ok) {
        const data = await response.json();
        alert(`Registration successful! Welcome, ${data.full_name}. Please login.`);
        window.location.hash = "#/login";
      } else {
        const errorData = await response.json();
        console.error("Registration failed:", errorData);
        alert(`Registration failed: ${errorData.detail || "Unknown error"}`);
      }
    } catch (error) {
      console.error("An error occurred during registration:", error);
      alert("An error occurred during registration. Please check your network connection and make sure the server is running.");
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-gray-900 via-gray-800 to-gray-900 text-white flex flex-col items-center justify-center p-6">
      <div className="relative bg-gray-800/60 backdrop-blur-xl border border-gray-700/40 p-10 rounded-2xl shadow-2xl w-full max-w-md transform transition-all duration-300 hover:scale-[1.02] hover:shadow-blue-500/30">
        <h2 className="text-4xl font-extrabold mb-4 text-center text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-cyan-400 drop-shadow-[0_0_10px_rgba(59,130,246,0.5)]">
          Create an Account
        </h2>
        <p className="text-center text-gray-400 text-sm mb-6">
          Registration is required to access the Career Quiz
        </p>

        <form onSubmit={handleRegister} className="space-y-6">
          <div>
            <label
              htmlFor="name"
              className="block text-gray-300 mb-2 font-medium"
            >
              Full Name
            </label>
            <input
              id="name"
              type="text"
              className="w-full p-3 rounded-lg bg-gray-900/60 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div>
            <label
              htmlFor="email"
              className="block text-gray-300 mb-2 font-medium"
            >
              Email Address
            </label>
            <input
              id="email"
              type="email"
              className="w-full p-3 rounded-lg bg-gray-900/60 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-gray-300 mb-2 font-medium"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              className="w-full p-3 rounded-lg bg-gray-900/60 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              placeholder="********"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 mt-4 rounded-lg font-semibold bg-linear-to-r from-blue-600 to-cyan-500 text-white hover:from-blue-500 hover:to-cyan-400 shadow-lg shadow-blue-500/25 transition-all duration-300"
          >
            Register
          </button>
        </form>

        <p className="text-center text-gray-400 mt-6">
          Already have an account?{" "}
          <a
            href="#/login"
            className="text-blue-400 hover:text-cyan-300 font-medium transition"
          >
            Login
          </a>
        </p>
      </div>
    </div>
  );
};

export default Register;
