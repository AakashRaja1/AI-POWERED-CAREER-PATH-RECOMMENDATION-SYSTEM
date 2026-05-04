/*
Home page for the career recommendation system. It introduces the project and routes users toward login, registration, and the main tools.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

import React, { useEffect } from "react";

const BRAND_LOGO_SRC = "/brand-logo.svg";

const Logo = ({ className = "w-16 h-16" }) => (
  <img
    src={BRAND_LOGO_SRC}
    alt="AI Career Path Logo"
    className={className}
    loading="eager"
    decoding="async"
  />
);

const Home = () => {
  // Add favicon with the shared brand logo asset.
  useEffect(() => {
    let link = document.querySelector("link[rel='icon']");
    if (!link) {
      link = document.createElement("link");
      link.rel = "icon";
      document.head.appendChild(link);
    }
    link.type = "image/svg+xml";
    link.href = BRAND_LOGO_SRC;

    // Optional: touch icon for mobile
    let apple = document.querySelector("link[rel='apple-touch-icon']");
    if (!apple) {
      apple = document.createElement("link");
      apple.rel = "apple-touch-icon";
      document.head.appendChild(apple);
    }
    apple.href = BRAND_LOGO_SRC;
  }, []);

  return (
    <div className="relative min-h-screen bg-white overflow-hidden">
      {/* Decorative animated background blobs (matching Dashboard theme) */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-36 -left-36 w-96 h-96 rounded-full bg-linear-to-br from-violet-200/50 to-transparent blur-3xl" />
        <div className="absolute top-1/4 -right-28 w-80 h-80 rounded-full bg-linear-to-bl from-blue-200/50 to-transparent blur-3xl" />
        <div className="absolute -bottom-36 left-1/2 w-96 h-96 rounded-full bg-linear-to-tr from-emerald-200/50 to-transparent blur-3xl" />
      </div>

      <div className="relative z-10 flex flex-col items-center justify-center px-4 py-16 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center max-w-5xl mx-auto">
          <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-linear-to-r from-violet-100 to-purple-100 border border-violet-200 mb-6">
            <Logo className="w-20 h-20" />
            <span className="text-sm font-semibold text-violet-700">AI Career Path</span>
          </div>

          <h1 className="text-5xl sm:text-6xl font-black bg-linear-to-r from-violet-600 via-purple-600 to-fuchsia-600 bg-clip-text text-transparent mb-6 leading-tight">
            Discover Your Perfect Career
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
            AI-powered career guidance tailored to your unique skills, interests, and personality.
          </p>

          {/* CTA area — keep the same buttons but style to match Dashboard */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-12">
            <a
              href="#/register"
              className="group mt-2 sm:mt-0 w-full sm:w-auto py-3 px-6 rounded-xl bg-linear-to-r from-violet-500 via-purple-500 to-fuchsia-500 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 text-center"
            >
              Get Started
            </a>
            <a
              href="#/login"
              className="mt-2 sm:mt-0 w-full sm:w-auto py-3 px-6 rounded-xl bg-white/10 backdrop-blur-md hover:bg-white/20 text-gray-900 font-semibold shadow transition-all duration-300 border border-gray-200"
            >
              Sign In
            </a>
            <a
              href="#/admin-login"
              className="mt-2 sm:mt-0 w-full sm:w-auto py-3 px-6 rounded-xl bg-black/30 backdrop-blur-md hover:bg-black/45 text-white font-semibold shadow transition-all duration-300 border border-amber-300/40"
            >
              Admin Login
            </a>
          </div>
        </div>

        {/* Feature Cards — restyled to match Dashboard cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto mt-16">
          <div className="relative rounded-3xl overflow-hidden transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 bg-white">
            <div className="p-6 h-full">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">AI-Powered Insights</h3>
              <p className="text-sm text-gray-600">Advanced algorithms analyze your profile to recommend the best career matches</p>
            </div>
          </div>

          <div className="relative rounded-3xl overflow-hidden transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 bg-white">
            <div className="p-6 h-full">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Personalized Roadmap</h3>
              <p className="text-sm text-gray-600">Get a detailed 5-year career growth plan tailored to your goals</p>
            </div>
          </div>

          <div className="relative rounded-3xl overflow-hidden transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 bg-white">
            <div className="p-6 h-full">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">24/7 AI Assistant</h3>
              <p className="text-sm text-gray-600">Chat with our AI career advisor anytime for instant guidance</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
