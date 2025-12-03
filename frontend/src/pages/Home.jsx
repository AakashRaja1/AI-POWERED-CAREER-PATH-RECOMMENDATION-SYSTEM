import React, { useState, useEffect } from "react";

// SVG string for favicon (same visual as Logo component, without <text> for clarity at small sizes)
const LOGO_SVG = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="grad" x1="0" y1="64" x2="64" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#2563EB" />
      <stop offset="0.5" stop-color="#7C3AED" />
      <stop offset="1" stop-color="#EC4899" />
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="black" opacity="0.6"/>
  <circle cx="32" cy="32" r="28" stroke="url(#grad)" stroke-width="3" fill="none" opacity="0.5" />
  <circle cx="16" cy="40" r="3" fill="#ffffff" />
  <circle cx="28" cy="28" r="3" fill="#ffffff" />
  <circle cx="40" cy="20" r="3" fill="#ffffff" />
  <circle cx="48" cy="12" r="2.5" fill="#ffffff" />
  <path d="M16 40 L28 28 L40 20 L48 12" stroke="url(#grad)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path d="M22 44 C30 36, 36 30, 48 24" stroke="url(#grad)" stroke-width="3" stroke-linecap="round" fill="none" />
  <path d="M46 20 L52 22 L48 24" fill="url(#grad)" />
</svg>
`;

const Logo = ({ className = "w-16 h-16" }) => (
  <svg
    className={className}
    viewBox="0 0 64 64"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-label="AI Career Path Logo"
  >
    <defs>
      <linearGradient id="grad" x1="0" y1="64" x2="64" y2="0" gradientUnits="userSpaceOnUse">
        <stop stopColor="#2563EB" />
        <stop offset="0.5" stopColor="#7C3AED" />
        <stop offset="1" stopColor="#EC4899" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" stroke="url(#grad)" strokeWidth="3" opacity="0.35" />
    {/* Nodes */}
    <circle cx="16" cy="40" r="3" fill="#fff" opacity="0.9" />
    <circle cx="28" cy="28" r="3" fill="#fff" opacity="0.9" />
    <circle cx="40" cy="20" r="3" fill="#fff" opacity="0.9" />
    <circle cx="48" cy="12" r="2.5" fill="#fff" opacity="0.9" />
    {/* Connections */}
    <path d="M16 40 L28 28 L40 20 L48 12" stroke="url(#grad)" strokeWidth="2.5" strokeLinecap="round" />
    {/* Upward arrow representing growth */}
    <path d="M22 44 C30 36, 36 30, 48 24" stroke="url(#grad)" strokeWidth="3" strokeLinecap="round" fill="none" />
    <path d="M46 20 L52 22 L48 24" fill="url(#grad)" />
    {/* Subtext mark */}
    <text x="32" y="54" textAnchor="middle" fontSize="8" fill="#ffffff" opacity="0.9">
      AI Career
    </text>
  </svg>
);

const Home = () => {
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    const stored = localStorage.getItem("userName");
    if (token && stored) {
      const nameOnly = stored.includes("@") ? stored.split("@")[0] : stored;
      setUserName(nameOnly);
    } else {
      setUserName("");
    }
  }, []);

  // Add favicon with our logo (replaces React/Vite icon in the tab)
  useEffect(() => {
    const svgDataUrl = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(LOGO_SVG);
    let link = document.querySelector("link[rel='icon']");
    if (!link) {
      link = document.createElement("link");
      link.rel = "icon";
      document.head.appendChild(link);
    }
    link.type = "image/svg+xml";
    link.href = svgDataUrl;

    // Optional: touch icon for mobile
    let apple = document.querySelector("link[rel='apple-touch-icon']");
    if (!apple) {
      apple = document.createElement("link");
      apple.rel = "apple-touch-icon";
      document.head.appendChild(apple);
    }
    apple.href = svgDataUrl;
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("userName");
    localStorage.removeItem("token");
    localStorage.removeItem("isAdmin");
    setUserName("");
    window.location.hash = "#/";
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
        {/* Dark overlay for better text readability */}
        <div className="absolute inset-0 bg-linear-to-br from-blue-900/80 via-purple-900/70 to-pink-900/80"></div>
        {/* Animated gradient overlay */}
        <div className="absolute inset-0 bg-linear-to-t from-black/40 to-transparent"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4 py-16 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center max-w-4xl mx-auto animate-fadeIn">
          {/* Project Logo */}
          <div className="flex items-center justify-center mb-6">
            <Logo className="w-20 h-20 drop-shadow-2xl" />
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6 drop-shadow-2xl">
            Discover Your Perfect
            <span className="block text-transparent bg-linear-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text mt-2">
              Career Path
            </span>
          </h1>
          <p className="text-xl sm:text-2xl text-gray-200 mb-8 drop-shadow-lg leading-relaxed">
            AI-powered career guidance tailored to your unique skills, interests,
            and personality
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-12">
            <a
              href="#/register"
              className="group bg-linear-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-10 rounded-full text-lg transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-blue-500/50 w-full sm:w-auto"
            >
              <span className="flex items-center justify-center gap-2">
                Get Started
                <span className="group-hover:translate-x-1 transition-transform">
                  &rarr;
                </span>
              </span>
            </a>
            <a
              href="#/login"
              className="bg-white/10 backdrop-blur-md hover:bg-white/20 text-white font-bold py-4 px-10 rounded-full text-lg transition-all duration-300 transform hover:scale-105 shadow-2xl border-2 border-white/30 hover:border-white/50 w-full sm:w-auto"
            >
              Sign In
            </a>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto mt-20 animate-slideUp">
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-300 transform hover:-translate-y-2 hover:shadow-2xl">
            <div className="text-5xl mb-4">🎯</div>
            <h3 className="text-xl font-bold text-white mb-2">
              AI-Powered Insights
            </h3>
            <p className="text-gray-300 text-sm">
              Advanced algorithms analyze your profile to recommend the best
              career matches
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-300 transform hover:-translate-y-2 hover:shadow-2xl">
            <div className="text-5xl mb-4">📊</div>
            <h3 className="text-xl font-bold text-white mb-2">
              Personalized Roadmap
            </h3>
            <p className="text-gray-300 text-sm">
              Get a detailed 5-year career growth plan tailored to your goals
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-300 transform hover:-translate-y-2 hover:shadow-2xl">
            <div className="text-5xl mb-4">🤖</div>
            <h3 className="text-xl font-bold text-white mb-2">
              24/7 AI Assistant
            </h3>
            <p className="text-gray-300 text-sm">
              Chat with our AI career advisor anytime for instant guidance
            </p>
          </div>
        </div>

        {/* Stats Section */}
        {/* <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto mt-16">
          <div className="text-center">
            <div className="text-4xl font-bold text-white mb-2">10K+</div>
            <div className="text-gray-300 text-sm">Career Assessments</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-white mb-2">95%</div>
            <div className="text-gray-300 text-sm">Satisfaction Rate</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-white mb-2">50+</div>
            <div className="text-gray-300 text-sm">Career Paths</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-white mb-2">24/7</div>
            <div className="text-gray-300 text-sm">AI Support</div>
          </div>
        </div> */}
      </div>

      {/* Floating Particles Effect */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
        <div
          className="absolute w-2 h-2 bg-white/30 rounded-full top-1/4 left-1/4 animate-ping"
          style={{ animationDuration: "3s" }}
        ></div>
        <div
          className="absolute w-2 h-2 bg-blue-400/30 rounded-full top-1/3 right-1/4 animate-ping"
          style={{ animationDuration: "4s", animationDelay: "1s" }}
        ></div>
        <div
          className="absolute w-2 h-2 bg-purple-400/30 rounded-full bottom-1/4 left-1/3 animate-ping"
          style={{ animationDuration: "5s", animationDelay: "2s" }}
        ></div>
      </div>
    </div>
  );
};

export default Home;
