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
        {/* Main Heading - NEW */}
        <div className="max-w-7xl mx-auto mb-6 text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
            Right Career Bright Future
          </h1>
          <p className="text-gray-600 text-lg">Your personalized career guidance dashboard</p>
        </div>

        {/* Header with Welcome Message */}
        <div className="max-w-7xl mx-auto mb-8">
          <div className="bg-white/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-gray-200">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
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
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-md"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        {/* Profile & Quick Actions */}
        <div className="max-w-7xl mx-auto mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Profile Card */}
            <div className="bg-white/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">👤</span>
                <h3 className="text-xl font-bold text-gray-800">Your Profile</h3>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 text-sm">Name:</span>
                  <span className="font-semibold text-gray-800">{userName || "Not set"}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 text-sm">Email:</span>
                  <span className="font-semibold text-gray-800 text-sm truncate max-w-[180px]">{userEmail}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600 text-sm">Status:</span>
                  <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold">Active</span>
                </div>
              </div>
              <button className="mt-4 w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300">
                Edit Profile
              </button>
            </div>

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

        {/* Recent Activity / Statistics */}
        <div className="max-w-7xl mx-auto">
          <div className="bg-white/80 backdrop-blur-md rounded-2xl p-8 shadow-lg border border-gray-200">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">📊 Your Career Journey</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl">
                <div className="text-4xl mb-2">🎓</div>
                <div className="text-3xl font-bold text-blue-600">0</div>
                <div className="text-sm text-gray-600 mt-1">Assessments Taken</div>
              </div>
              <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl">
                <div className="text-4xl mb-2">💬</div>
                <div className="text-3xl font-bold text-purple-600">0</div>
                <div className="text-sm text-gray-600 mt-1">AI Chats</div>
              </div>
              <div className="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-xl">
                <div className="text-4xl mb-2">📚</div>
                <div className="text-3xl font-bold text-green-600">0</div>
                <div className="text-sm text-gray-600 mt-1">Courses Recommended</div>
              </div>
              <div className="text-center p-6 bg-gradient-to-br from-pink-50 to-pink-100 rounded-xl">
                <div className="text-4xl mb-2">⭐</div>
                <div className="text-3xl font-bold text-pink-600">0</div>
                <div className="text-sm text-gray-600 mt-1">Skills Identified</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
