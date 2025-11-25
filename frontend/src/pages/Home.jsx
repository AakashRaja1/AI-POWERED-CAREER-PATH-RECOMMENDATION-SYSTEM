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
      // Clear userName if no token
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
    <div className="min-h-screen bg-neutral-900 text-gray-100 font-poppins">
      {/* ===== NAVBAR ===== */}
      <nav className="flex justify-between items-center px-8 py-5 bg-neutral-900/70 backdrop-blur-xl border-b border-neutral-800 shadow-md fixed top-0 left-0 w-full z-50">
        <a href="#/" className="text-2xl font-extrabold text-blue-400 drop-shadow-sm">
          AI CareerPath
        </a>
        <div className="flex items-center gap-3">
          {userName ? (
            <>
              <span className="hidden sm:block text-gray-400 text-sm">
                Hi, <span className="text-blue-400 font-semibold">{userName}</span>
              </span>
              {localStorage.getItem("isAdmin") === "true" && (
                <a
                  href="#/admin"
                  className="bg-red-500 hover:bg-red-600 text-white font-medium px-5 py-2 rounded-lg transition-all duration-300 hover:scale-[1.03] shadow-md hover:shadow-red-500/20"
                >
                  Admin
                </a>
              )}
              <button
                onClick={handleLogout}
                className="bg-neutral-700 hover:bg-neutral-600 text-gray-100 font-medium px-5 py-2 rounded-lg transition-all duration-300 hover:scale-[1.03] shadow-md hover:shadow-neutral-500/20"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <a
                href="#/login"
                className="bg-neutral-700 hover:bg-neutral-600 text-gray-100 font-medium px-5 py-2 rounded-lg transition-all duration-300 hover:scale-[1.03] shadow-md hover:shadow-neutral-500/20"
              >
                Login
              </a>
              <a
                href="#/register"
                className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-5 rounded-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30"
              >
                Register
              </a>
              <a
                href="#/admin-login"
                className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-5 rounded-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-red-500/30"
              >
                Admin
              </a>
            </>
          )}
        </div>
      </nav>

      {/* ===== HERO SECTION ===== */}
      <section className="relative flex flex-col items-center justify-center text-center min-h-screen px-6 pt-24">
        <img
          src="https://images.unsplash.com/photo-1555949963-aa79dcee981d?auto=format&fit=crop&w=1920&q=80"
          alt="AI Career Background"
          className="absolute inset-0 w-full h-full object-cover opacity-40"
        />
        <div className="absolute inset-0 bg-linear-to-b from-neutral-900/80 via-neutral-900/70 to-black"></div>

        <div className="relative z-10 max-w-2xl animate-fadeIn">
          <h2 className="text-4xl sm:text-5xl font-extrabold mb-6 leading-tight drop-shadow-md">
            Discover Your Future with{" "}
            <span className="text-blue-400">AI Precision</span>
          </h2>
          <p className="text-gray-300 text-lg sm:text-xl mb-10 leading-relaxed">
            Our AI-powered system analyzes your skills, education, and interests
            to recommend the most suitable career paths — personalized just for
            you.
          </p>
          {userName ? (
            <a
              href="#/form"
              className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30"
            >
              🚀 Start Career Test
            </a>
          ) : (
            <div className="space-y-4">
              <p className="text-gray-400 text-sm mb-4">
                Please register and login to access the Career Quiz
              </p>
              <div className="flex gap-4 justify-center">
                <a
                  href="#/register"
                  className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30"
                >
                  📝 Register First
                </a>
                <a
                  href="#/login"
                  className="inline-block bg-neutral-700 hover:bg-neutral-600 text-white font-semibold py-3 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105"
                >
                  🔐 Login
                </a>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ===== FEATURES SECTION ===== */}
      <section className="py-20 px-6 bg-linear-to-b from-neutral-900 to-neutral-950 text-center">
        <h3 className="text-3xl sm:text-4xl font-bold mb-6 text-gray-100 drop-shadow-sm">
          How It Works
        </h3>
        <p className="max-w-3xl mx-auto text-gray-400 text-lg mb-12">
          AI CareerPath is your personal career advisor powered by artificial
          intelligence. It studies your education, strengths, and interests to
          help you make smarter career decisions — guiding you toward success
          with precision and confidence.
        </p>

        {/* Features Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {[
            {
              title: "Smart Recommendations",
              desc: "Our AI learns from your input and suggests the most relevant career paths tailored to you.",
              icon: "🤖",
            },
            {
              title: "Skill-Based Analysis",
              desc: "We evaluate your education, interests, and talents to align them with your future goals.",
              icon: "🎯",
            },
            {
              title: "Accurate & Personalized",
              desc: "Every recommendation is unique — because your career journey deserves precision.",
              icon: "🌟",
            },
          ].map((item, i) => (
            <div
              key={i}
              className="bg-neutral-800/50 border border-neutral-700 rounded-2xl p-8 shadow-lg hover:shadow-blue-500/20 transition-all duration-300 hover:scale-[1.03]"
            >
              <div className="text-4xl mb-4">{item.icon}</div>
              <h4 className="text-xl font-semibold mb-3 text-gray-100">
                {item.title}
              </h4>
              <p className="text-gray-400">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className="py-6 text-center text-gray-500 border-t border-neutral-800 bg-neutral-950">
        <p>
          © {new Date().getFullYear()} AI CareerPath — Powered by{" "}
          <span className="text-blue-400 font-semibold">Artificial Intelligence</span>
        </p>
      </footer>
    </div>
  );
};

export default Home;
