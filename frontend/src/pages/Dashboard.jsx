/*
User dashboard page. It shows saved predictions and gives the user quick access to core career tools.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

import React from "react";

const MODULES = [
  {
    id: "behavior",
    title: "Personality Analysis",
    icon: "👤",
    description:
      "Discover your unique personality traits through video analysis. Understand your strengths, work style, and behavioral patterns.",
    action: "Start Analysis",
    href: "#/behavior",
    accent: "from-violet-500 via-purple-500 to-fuchsia-500",
    badge: "01",
    bgAccent: "bg-violet-50",
  },
  {
    id: "career-path",
    title: "Career Path",
    icon: "🎯",
    description:
      "Get personalized career recommendations based on your personality analysis. Explore pathways tailored to your unique profile.",
    action: "View Career Path",
    href: "#/form",
    accent: "from-blue-500 via-cyan-500 to-teal-500",
    badge: "02",
    bgAccent: "bg-blue-50",
  },
  {
    id: "scholarships",
    title: "Scholarship Finder",
    icon: "🎓",
    description:
      "Find scholarships and funding opportunities that match your profile. Filter by level, country, and funding type.",
    action: "Explore Scholarships",
    href: "#/scholarships",
    accent: "from-emerald-500 via-green-500 to-lime-500",
    badge: "03",
    bgAccent: "bg-emerald-50",
  },
  {
    id: "assistant",
    title: "AI Assistant",
    icon: "🤖",
    description:
      "Chat with our AI to get instant answers about careers, education, and your personal development journey.",
    action: "Open Assistant",
    href: "#/chatbot",
    accent: "from-orange-500 via-amber-500 to-yellow-500",
    badge: "04",
    bgAccent: "bg-orange-50",
  },
];

const Dashboard = () => {
  return (
    <div className="relative min-h-screen bg-white overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-linear-to-br from-violet-200/50 to-transparent blur-3xl" />
        <div className="absolute top-1/4 -right-32 w-80 h-80 rounded-full bg-linear-to-bl from-blue-200/50 to-transparent blur-3xl" />
        <div className="absolute -bottom-40 left-1/2 w-96 h-96 rounded-full bg-linear-to-tr from-emerald-200/50 to-transparent blur-3xl" />
      </div>

      <div className="relative z-10">
        {/* Hero Section */}
        <section className="px-4 py-12 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-6xl">
            <div className="text-center mb-16">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-linear-to-r from-violet-100 to-purple-100 border border-violet-200 mb-6">
                <span className="text-2xl">✨</span>
                <span className="text-sm font-semibold text-violet-700">Welcome to Your Career Journey</span>
              </div>
              <h1 className="text-5xl sm:text-6xl font-black bg-linear-to-r from-violet-600 via-purple-600 to-fuchsia-600 bg-clip-text text-transparent mb-6 leading-tight">
                Find Your Perfect Career
              </h1>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
                Follow a guided path through personality analysis, career exploration, scholarships, and AI-powered guidance. Your personalized career journey starts here.
              </p>
            </div>

            {/* Main Modules Grid */}
            <div className="grid gap-6 lg:grid-cols-4 mb-12">
              {MODULES.map((module) => (
                <div
                  key={module.id}
                  className="group relative"
                >
                  {/* Card */}
                  <div className={`relative h-full rounded-3xl overflow-hidden transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 ${module.bgAccent}`}>
                    {/* Gradient Border */}
                    <div className={`absolute inset-0 bg-linear-to-br ${module.accent} rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10`} />
                    
                    <div className="relative p-6 h-full bg-white rounded-3xl group-hover:bg-opacity-95 transition-all duration-300 flex flex-col">
                      {/* Badge */}
                      <div className="flex items-start justify-between mb-4">
                        <div className={`inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-linear-to-br ${module.accent} text-white text-lg font-bold shadow-lg`}>
                          {module.badge}
                        </div>
                        <span className="text-3xl">{module.icon}</span>
                      </div>

                      {/* Content */}
                      <h3 className="text-xl font-bold text-gray-900 mb-3">
                        {module.title}
                      </h3>
                      <p className="text-sm text-gray-600 leading-relaxed grow">
                        {module.description}
                      </p>

                      {/* Button */}
                      <button
                        onClick={() => window.location.hash = module.href}
                        className={`mt-6 w-full py-3 px-4 rounded-xl bg-linear-to-r ${module.accent} text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 text-center`}
                      >
                        {module.action}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Journey Steps */}
            <div className="bg-linear-to-r from-slate-900 via-slate-800 to-slate-900 rounded-3xl p-8 sm:p-12 overflow-hidden relative">
              <div className="absolute inset-0 opacity-10">
                <div className="absolute inset-0 bg-grid-white/[0.02]" />
              </div>

              <div className="relative z-10">
                <h2 className="text-3xl sm:text-4xl font-bold text-white mb-12 text-center">
                  Your Recommended Journey
                </h2>

                <div className="grid gap-6 md:grid-cols-4">
                  {[
                    {
                      step: "1",
                      title: "Personality Analysis",
                      desc: "Upload a video for personality assessment",
                      icon: "👤",
                    },
                    {
                      step: "2",
                      title: "Career Path",
                      desc: "Discover careers based on your traits",
                      icon: "🎯",
                    },
                    {
                      step: "3",
                      title: "Scholarships",
                      desc: "Find funding for your education",
                      icon: "🎓",
                    },
                    {
                      step: "4",
                      title: "AI Assistant",
                      desc: "Get ongoing guidance and support",
                      icon: "🤖",
                    },
                  ].map((item, idx) => (
                    <div key={idx} className="text-center">
                      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-linear-to-br from-violet-500 to-fuchsia-500 text-white text-2xl font-bold mb-4 shadow-lg">
                        {item.step}
                      </div>
                      <p className="text-lg font-semibold text-white">{item.title}</p>
                      <p className="text-sm text-gray-300 mt-2">{item.desc}</p>
                      <span className="text-3xl mt-2 block">{item.icon}</span>
                    </div>
                  ))}
                </div>

                <p className="text-center text-gray-300 mt-8 text-sm">
                  ⏱️ Estimated completion time: <span className="font-semibold">2-3 hours</span>
                </p>
              </div>
            </div>

            {/* Stats Section */}
            <div className="grid gap-6 md:grid-cols-3 my-12">
              <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 hover:shadow-xl transition-shadow">
                <div className="text-4xl font-bold bg-linear-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent mb-2">
                  100%
                </div>
                <p className="text-gray-600 font-medium">Personalized</p>
                <p className="text-sm text-gray-500 mt-2">Each recommendation is unique to you</p>
              </div>
              <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 hover:shadow-xl transition-shadow">
                <div className="text-4xl font-bold bg-linear-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent mb-2">
                  10K+
                </div>
                <p className="text-gray-600 font-medium">Career Options</p>
                <p className="text-sm text-gray-500 mt-2">Explore thousands of career paths</p>
              </div>
              <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 hover:shadow-xl transition-shadow">
                <div className="text-4xl font-bold bg-linear-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent mb-2">
                  24/7
                </div>
                <p className="text-gray-600 font-medium">AI Support</p>
                <p className="text-sm text-gray-500 mt-2">Get answers anytime you need</p>
              </div>
            </div>

            {/* Footer */}
            <div className="text-center py-8 border-t border-gray-200 mt-12">
              <p className="text-gray-600">
                Ready to discover your ideal career?
                <span className="font-semibold text-transparent bg-linear-to-r from-violet-600 to-fuchsia-600 bg-clip-text"> Start with Personality Analysis</span>
              </p>
              <p className="text-xs text-gray-500 mt-4">
                © 2025 AI Career Path Recommendation System | Built for Your Future 🚀
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
