import React, { useEffect, useMemo, useState } from "react";

const MODULES = [
  {
    id: "behavior",
    title: "Career According to Your Personality",
    icon: "👤",
    description:
      "Understand your personality patterns and translate them into career directions that fit you better.",
    action: "Start Analysis",
    href: "#/behavior",
    accent: "from-orange-500 to-rose-500",
    badge: "01",
  },
  {
    id: "scholarships",
    title: "Find Scholarship",
    icon: "🎓",
    description:
      "Search opportunities by level, country, institution type, and funding to support your next step.",
    action: "Explore Scholarships",
    href: "#/scholarships",
    accent: "from-emerald-500 to-cyan-500",
    badge: "02",
  },
  {
    id: "career-path",
    title: "Career Path",
    icon: "🎯",
    description:
      "Use the recommendation system to discover a career path that aligns with your interests and skills.",
    action: "Start Assessment",
    href: "#/form",
    accent: "from-blue-500 to-indigo-500",
    badge: "03",
  },
  {
    id: "assistant",
    title: "AI Assistant",
    icon: "🤖",
    description:
      "Ask career questions anytime and get instant guidance from the built-in assistant.",
    action: "Open Assistant",
    href: "#/chatbot",
    accent: "from-purple-500 to-fuchsia-500",
    badge: "04",
  },
];

const Dashboard = () => {
  const [userName, setUserName] = useState("");
  const [userEmail, setUserEmail] = useState("");

  useEffect(() => {
    const storedName = localStorage.getItem("userName");
    const email = localStorage.getItem("userEmail") || "";

    setUserEmail(email);

    if (storedName && storedName !== email) {
      setUserName(storedName);
    } else if (email) {
      const namePart = email.split("@")[0];
      const formattedName = namePart
        .replace(/[._]/g, " ")
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(" ");
      setUserName(formattedName);
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
    window.location.hash = "#/";
  };

  const userInitial = useMemo(() => (userName ? userName.charAt(0).toUpperCase() : "U"), [userName]);

  return (
    <div className="relative min-h-screen overflow-hidden bg-linear-to-br from-slate-50 via-sky-50 to-indigo-100 text-slate-900">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-24 -left-20 h-72 w-72 rounded-full bg-sky-300/30 blur-3xl" />
        <div className="absolute top-32 -right-24 h-80 w-80 rounded-full bg-fuchsia-300/25 blur-3xl" />
        <div className="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-emerald-300/20 blur-3xl" />
      </div>

      <div className="relative z-10 px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <section className="mx-auto mb-6 max-w-7xl overflow-hidden rounded-[2rem] border border-white/70 bg-slate-950/90 text-white shadow-[0_30px_80px_-25px_rgba(15,23,42,0.65)] backdrop-blur-xl">
          <div className="grid gap-8 px-6 py-8 sm:px-8 lg:grid-cols-[1.4fr_0.9fr] lg:px-10 lg:py-10">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-sky-100">
                Career dashboard
              </div>
              <div className="space-y-4">
                <h1 className="max-w-3xl text-3xl font-semibold leading-tight sm:text-4xl lg:text-5xl">
                  Build a clear next step with a cleaner, calmer dashboard.
                </h1>
                <p className="max-w-2xl text-sm leading-7 text-slate-300 sm:text-base">
                  Move through personality analysis, scholarships, career path recommendations, and AI guidance in a simple sequence that keeps the experience focused.
                </p>
              </div>
              <div className="flex flex-wrap gap-3 text-sm">
                <span className="rounded-full bg-white/10 px-4 py-2 text-slate-100 ring-1 ring-white/10">Personalized</span>
                <span className="rounded-full bg-white/10 px-4 py-2 text-slate-100 ring-1 ring-white/10">Modern UI</span>
                <span className="rounded-full bg-white/10 px-4 py-2 text-slate-100 ring-1 ring-white/10">Fast access</span>
              </div>
            </div>

            <div className="rounded-[1.75rem] border border-white/10 bg-white/8 p-5 shadow-2xl shadow-black/10">
              <div className="flex items-center gap-4">
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-400 via-indigo-500 to-fuchsia-500 text-2xl font-bold text-white shadow-lg shadow-sky-500/30">
                  {userInitial}
                </div>
                <div className="min-w-0">
                  <p className="text-sm uppercase tracking-[0.2em] text-sky-200">Signed in as</p>
                  <h2 className="mt-1 truncate text-2xl font-semibold text-white">{userName}</h2>
                  <p className="truncate text-sm text-slate-300">{userEmail || "Email not available"}</p>
                </div>
              </div>

              <div className="mt-5 grid grid-cols-3 gap-3 text-center text-xs text-slate-300">
                <div className="rounded-2xl bg-white/8 p-3 ring-1 ring-white/10">
                  <div className="text-base font-semibold text-white">4</div>
                  Modules
                </div>
                <div className="rounded-2xl bg-white/8 p-3 ring-1 ring-white/10">
                  <div className="text-base font-semibold text-white">AI</div>
                  Guided
                </div>
                <div className="rounded-2xl bg-white/8 p-3 ring-1 ring-white/10">
                  <div className="text-base font-semibold text-white">24/7</div>
                  Support
                </div>
              </div>

              <button
                onClick={handleLogout}
                className="mt-5 w-full rounded-2xl border border-white/10 bg-white px-4 py-3 font-semibold text-slate-900 transition hover:-translate-y-0.5 hover:bg-slate-100"
              >
                Logout
              </button>
            </div>
          </div>
        </section>

        <section className="mx-auto mb-6 max-w-7xl">
          <div className="flex items-end justify-between gap-4 mb-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.22em] text-slate-500">Module sequence</p>
              <h3 className="mt-1 text-2xl font-semibold text-slate-900">Follow the recommended flow</h3>
            </div>
          </div>

          <div className="grid gap-5 lg:grid-cols-2 xl:grid-cols-4">
            {MODULES.map((module) => (
              <article
                key={module.id}
                className="group relative overflow-hidden rounded-[1.75rem] border border-white/80 bg-white/85 p-6 shadow-[0_20px_60px_-25px_rgba(15,23,42,0.25)] backdrop-blur-md transition duration-300 hover:-translate-y-1 hover:shadow-[0_30px_70px_-28px_rgba(15,23,42,0.35)]"
              >
                <div className={`absolute inset-x-0 top-0 h-1 bg-gradient-to-r ${module.accent}`} />
                <div className="mb-5 flex items-start justify-between gap-3">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-950 text-2xl text-white shadow-lg shadow-slate-900/15">
                    {module.icon}
                  </div>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-500">
                    {module.badge}
                  </span>
                </div>
                <h4 className="text-xl font-semibold text-slate-900">{module.title}</h4>
                <p className="mt-3 min-h-16 text-sm leading-6 text-slate-600">{module.description}</p>
                <button
                  onClick={() => window.location.hash = module.href}
                  className={`mt-6 inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-r ${module.accent} px-4 py-3 text-sm font-semibold text-white transition duration-300 hover:brightness-110`}
                >
                  {module.action}
                </button>
              </article>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl">
          <div className="grid gap-5 md:grid-cols-3">
            <div className="rounded-[1.5rem] border border-white/70 bg-white/80 p-5 shadow-lg backdrop-blur-md">
              <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">Step 1</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">Personality first</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">Start with behavior analysis to make the rest of the recommendations feel more personal and accurate.</p>
            </div>
            <div className="rounded-[1.5rem] border border-white/70 bg-white/80 p-5 shadow-lg backdrop-blur-md">
              <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">Step 2</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">Funding support</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">Look for scholarships early so career planning and education planning can move together.</p>
            </div>
            <div className="rounded-[1.5rem] border border-white/70 bg-white/80 p-5 shadow-lg backdrop-blur-md">
              <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">Step 3</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">Guidance loop</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">Use the career path flow and AI assistant to refine choices and stay supported.
              </p>
            </div>
          </div>
        </section>

        <footer className="mx-auto mt-8 max-w-7xl rounded-[1.5rem] border border-white/70 bg-white/75 p-5 text-center shadow-lg backdrop-blur-md">
          <p className="text-sm text-slate-600">
            Powered by <span className="font-semibold text-slate-900">AI Intelligence</span>
          </p>
          <p className="mt-1 text-xs text-slate-500">
            © 2025 Final Year Project: Career Path Recommendation System.
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Dashboard;
