import React, { useState, useEffect } from "react";

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

  const handleLogout = () => {
    localStorage.removeItem("userName");
    localStorage.removeItem("token");
    localStorage.removeItem("isAdmin");
    setUserName("");
    window.location.hash = "#/";
  };

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img
          src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1920&q=80"
          alt="Career Success"
          className="w-full h-full object-cover"
        />
        {/* Dark overlay for better text readability */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/80 via-purple-900/70 to-pink-900/80"></div>
        {/* Animated gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4 py-16 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center max-w-4xl mx-auto animate-fadeIn">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-white mb-6 drop-shadow-2xl">
            Discover Your Perfect
            <span className="block text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text mt-2">
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
              className="group bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-10 rounded-full text-lg transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-blue-500/50 w-full sm:w-auto"
            >
              <span className="flex items-center justify-center gap-2">
                Get Started 
                <span className="group-hover:translate-x-1 transition-transform">
                  →
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
