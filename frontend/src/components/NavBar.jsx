import React, { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/behavior", label: "Behavior" },
  { to: "/form", label: "Career" },
  { to: "/scholarships", label: "Scholarships" },
  { to: "/chatbot", label: "Chatbot" },
];

const NavBar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState({ name: "", email: "" });

  useEffect(() => {
    const userName = localStorage.getItem("userName") || "";
    const userEmail = localStorage.getItem("userEmail") || "";
    setUser({ name: userName, email: userEmail });
  }, []);

  const handleLogout = () => {
    // Clear user authentication data
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("profile");
    localStorage.removeItem("cp_user_id");
    
    // Clear session behavior analysis data (but keep email-specific data for return logins)
    localStorage.removeItem("behavior_analysis_result");
    localStorage.removeItem("behavior_analysis_timestamp");
    
    // Clear user-specific data last so email-based keys stay intact
    const userEmail = localStorage.getItem("userEmail");
    localStorage.removeItem("userName");
    localStorage.removeItem("userEmail");
    
    navigate("/login");
  };

  return (
    <header className="w-full sticky top-0 bg-linear-to-r from-white via-slate-50 to-white/80 border-b shadow-md backdrop-blur">
      <div className="max-w-full mx-auto px-4 py-2 flex items-center gap-4">
        <div className="flex items-center gap-3 min-w-0">
          <img src="/brand-logo.svg" alt="logo" className="h-9 w-9 object-contain rounded-md" />
          <div className="ml-2 text-sm font-semibold text-gray-800 truncate">AI Career by Personality</div>
        </div>

        <nav className="flex-1">
          <ul className="flex gap-2 items-center text-sm overflow-x-auto scrollbar-hide">
            {links.map((l) => (
              <li key={l.to}>
                <Link
                  to={l.to}
                  className={`inline-flex items-center px-3 py-1 rounded-full text-gray-700 hover:text-gray-900 hover:shadow-sm transition ${location.pathname === l.to ? 'bg-indigo-50 text-indigo-700 font-medium' : 'bg-white/0'}`}
                >
                  {l.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="flex items-center gap-4">
          {user.name && (
            <div className="flex items-center gap-3 px-4 py-2 bg-linear-to-r from-indigo-50 to-purple-50 rounded-full border border-indigo-200 shadow-sm">
              <div className="flex flex-col justify-center">
                <div className="text-sm font-semibold text-gray-900">{user.name}</div>
                <div className="text-xs text-gray-600">{user.email}</div>
              </div>
              <button
                onClick={handleLogout}
                className="ml-2 px-3 py-1 bg-red-500 hover:bg-red-600 text-white text-xs font-medium rounded-full transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default NavBar;
