import React, { useState, useEffect } from "react";

const Dashboard = () => {
  const [userName, setUserName] = useState("");
  const [userEmail, setUserEmail] = useState("");

  useEffect(() => {
    const storedName = localStorage.getItem("userName");
    const email = localStorage.getItem("userEmail") || "";
    
    setUserEmail(email);
    
    if (storedName && storedName !== email) {
      // Use stored name if it exists and is not the email
      setUserName(storedName);
    } else if (email) {
      // Extract name from email (part before @)
      const namePart = email.split("@")[0];
      // Replace dots/underscores with spaces and capitalize each word
      const formattedName = namePart
        .replace(/[._]/g, " ")
        .split(" ")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(" ");
      setUserName(formattedName);
      // Save it for future use
      localStorage.setItem("userName", formattedName);
    } else {
      setUserName("Guest");
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userName");
    localStorage.removeItem("cp_user_id");
    window.location.hash = "#/"; // Changed from #/login to #/
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 -left-20 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 -right-20 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10 px-4 py-8 sm:px-6 lg:px-8">
        {/* Project Banner Section */}
        <div className="max-w-7xl mx-auto mb-8">
          <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl p-8 shadow-2xl">
            <div className="text-center">
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white mb-3">
                AI-Powered Career Path Recommendation System
              </h1>
              <p className="text-white/90 text-lg sm:text-xl max-w-3xl mx-auto">
                Discover your ideal career through advanced AI analysis of your skills, interests, and personality traits
              </p>
              <div className="flex flex-wrap justify-center gap-4 mt-6">
                <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                  <span className="text-white text-sm font-semibold">Smart Career Matching</span>
                </div>
                <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                  <span className="text-white text-sm font-semibold">Data-Driven Insights</span>
                </div>
                <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                  <span className="text-white text-sm font-semibold">5-Year Roadmap</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Header with Welcome Message */}
        <div className="max-w-7xl mx-auto mb-8">
          <div className="bg-white/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-gray-200">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              {/* Left: Welcome */}
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                  {userName.charAt(0) || "U"}
                </div>
                <div>
                  <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">
                    Welcome back, <span className="text-transparent bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text">{userName}</span>! 👋
                  </h1>
                  <p className="text-gray-600 text-sm mt-1">{userEmail}</p>
                </div>
              </div>

              {/* Right: Profile summary moved to top-right */}
              <div className="w-full sm:w-auto">
                <div className="bg-white/90 border border-gray-200 rounded-xl p-4 shadow flex flex-col gap-2 min-w-[280px]">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Name</span>
                    <span className="font-semibold text-gray-800">{userName}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Email</span>
                    <span className="font-semibold text-gray-800 text-xs truncate max-w-[160px]">{userEmail}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Status</span>
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold">Active</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="mt-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-300 w-full"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="max-w-7xl mx-auto mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Career Assessment Card */}
            <div className="bg-white/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">🎯</span>
                <h3 className="text-xl font-bold text-gray-800">Career Path</h3>
              </div>
              <p className="text-gray-600 text-sm mb-4">
                Discover your ideal career with our AI-powered recommendation system.
              </p>
              <button
                onClick={() => window.location.hash = "#/form"}
                className="w-full bg-gradient-to-r from-green-500 to-emerald-500 text-white py-2 rounded-lg font-semibold hover:from-green-600 hover:to-emerald-600 transition-all duration-300"
              >
                Start Assessment
              </button>
            </div>

            {/* AI Assistant Card */}
            <div className="bg-white/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">🤖</span>
                <h3 className="text-xl font-bold text-gray-800">AI Assistant</h3>
              </div>
              <p className="text-gray-600 text-sm mb-4">
                Get instant career guidance and answers to your questions 24/7.
              </p>
              <button
                onClick={() => window.location.hash = "#/chatbot"}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-2 rounded-lg font-semibold hover:from-purple-600 hover:to-pink-600 transition-all duration-300"
              >
                Chat Now
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="max-w-7xl mx-auto mt-12">
          <div className="bg-white/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-gray-200">
            <div className="text-center">
              <p className="text-gray-600 text-sm mb-2">
                Powered by <span className="font-semibold text-transparent bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text">AI Intelligence</span>
              </p>
              <p className="text-gray-500 text-xs">
                © 2025 Final Year Project: Career Path Recommendation System. All rights reserved.
              </p>
              <div className="mt-3 flex justify-center gap-4 text-xs text-gray-500">
                <a href="#" className="hover:text-blue-600 transition">Privacy Policy</a>
                <span>•</span>
                <a href="#" className="hover:text-blue-600 transition">Terms of Service</a>
                <span>•</span>
                <a href="#" className="hover:text-blue-600 transition">Contact Us</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
