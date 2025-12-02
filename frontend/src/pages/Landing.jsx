// frontend/src/pages/Landing.jsx
import React from "react";

const Landing = () => {
  return (
    <div className="relative min-h-screen bg-white text-gray-900 flex flex-col items-center justify-center font-poppins overflow-hidden">
      {/* ===== Background Image & Overlay ===== */}
      <img
        src="https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?auto=format&fit=crop&w=1920&q=80"
        alt="AI Background"
        className="absolute inset-0 w-full h-full object-cover opacity-10"
      />
      <div className="absolute inset-0 bg-linear-to-b from-white/80 via-white/70 to-white"></div>

      {/* ===== Content ===== */}
      <div className="relative z-10 text-center px-6 animate-fadeIn">
        <h1 className="text-4xl sm:text-6xl font-extrabold mb-6 leading-tight drop-shadow-md">
          Welcome to
          <br />
          <span className="text-blue-600">AI Career Path</span> Recommendation
          System
        </h1>
        <p className="text-gray-600 text-lg sm:text-xl mb-10 max-w-2xl mx-auto leading-relaxed">
          Unlock your future with AI-powered insights. Discover careers that
          perfectly match your personality, skills, and passions.
        </p>

        <div className="flex flex-wrap justify-center gap-6 mt-6">
          <a
            href="#/register"
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30"
          >
            🚀 Get Started
          </a>
          <a
            href="#/login"
            className="bg-gray-200 hover:bg-gray-300 text-gray-900 font-medium py-3 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-gray-400/20"
          >
            🔑 Login
          </a>
        </div>
      </div>

      {/* ===== Footer ===== */}
      <footer className="absolute bottom-6 text-gray-500 text-sm">
        © {new Date().getFullYear()} AI CareerPath — Built for your Future 🚀
      </footer>
    </div>
  );
};

export default Landing;
