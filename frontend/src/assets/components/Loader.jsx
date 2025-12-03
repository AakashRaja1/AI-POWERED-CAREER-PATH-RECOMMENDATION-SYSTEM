import React from "react";

const Loader = () => {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center z-50">
      {/* Background blur */}
      <div className="absolute inset-0 backdrop-blur-sm"></div>

      {/* Content */}
      <div className="relative z-10 text-center">
        {/* Animated gradient ring */}
        <div className="mb-8 inline-block">
          <div className="relative w-20 h-20 sm:w-24 sm:h-24">
            {/* Outer rotating ring */}
            <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-600 border-r-purple-600 animate-spin"></div>
            
            {/* Middle rotating ring (opposite direction) */}
            <div className="absolute inset-2 rounded-full border-4 border-transparent border-t-purple-600 border-r-pink-600 animate-spin" style={{ animationDirection: "reverse", animationDuration: "2s" }}></div>
            
            {/* Center circle with gradient */}
            <div className="absolute inset-4 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center">
              <div className="text-white text-2xl sm:text-3xl animate-bounce">🚀</div>
            </div>
          </div>
        </div>

        {/* Loading text */}
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-2">
          <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            Analyzing Your Profile
          </span>
        </h2>
        <p className="text-gray-600 text-sm sm:text-base mb-6">
          Our AI is finding your perfect career match...
        </p>

        {/* Animated dots */}
        <div className="flex justify-center gap-2">
          <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: "0s" }}></div>
          <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
          <div className="w-3 h-3 bg-pink-600 rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
        </div>

        {/* Progress bar */}
        <div className="mt-8 w-64 sm:w-80 h-1 bg-gray-200 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 animate-pulse" style={{ width: "100%", animation: "pulse 2s ease-in-out infinite" }}></div>
        </div>

        {/* Loading message */}
        <p className="text-gray-500 text-xs sm:text-sm mt-4">Processing your data securely...</p>
      </div>
    </div>
  );
};

export default Loader;
