/*
User avatar menu. It displays account actions and closes itself safely when the user clicks outside it.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const AvatarMenu = () => {
  const [open, setOpen] = useState(false);
  const [user, setUser] = useState({ name: "Guest", email: "" });
  const [rect, setRect] = useState(null);
  const navigate = useNavigate();
  const ref = useRef();

  useEffect(() => {
    const userName = localStorage.getItem("userName") || localStorage.getItem("user") || localStorage.getItem("profile");
    const userEmail = localStorage.getItem("userEmail") || "";
    
    if (userName) {
      setUser({ name: userName, email: userEmail });
    } else {
      setUser({ name: "Guest", email: "" });
    }

    function onDoc(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("click", onDoc);
    return () => document.removeEventListener("click", onDoc);
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("profile");
    localStorage.removeItem("userName");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("cp_user_id");
    setOpen(false);
    navigate("/login");
  };

  const login = () => {
    setOpen(false);
    navigate("/login");
  };

  const initials = (user.name || "G").split(" ").map(s => s[0]).slice(0, 2).join("").toUpperCase();

  const handleToggle = () => {
    if (ref.current) {
      const r = ref.current.getBoundingClientRect();
      setRect(r);
    }
    setOpen(o => !o);
  };

  const dropdownStyle = rect
    ? {
        position: "fixed",
        top: rect.bottom + 8 + window.scrollY,
        left: Math.min(rect.left, window.innerWidth - 16 - 240),
        zIndex: 9999,
        width: Math.min(240, window.innerWidth - 32),
      }
    : { position: "fixed", zIndex: 9999 };

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={handleToggle}
        className="h-9 w-9 rounded-full bg-gray-200 flex items-center justify-center text-sm font-semibold text-gray-700 hover:opacity-90"
        aria-label="User menu"
      >
        {initials}
      </button>

      {open && (
        <div style={dropdownStyle} className="bg-white border border-gray-200 rounded-lg shadow-xl z-50">
          <div className="p-4 border-b border-gray-100">
            <div className="text-sm font-semibold text-gray-900">{user.name}</div>
            <div className="text-xs text-gray-500 truncate mt-1">{user.email || "Email not available"}</div>
          </div>
          <div className="p-2">
            {user.email ? (
              <button onClick={logout} className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md font-medium transition">
                Logout
              </button>
            ) : (
              <button onClick={login} className="w-full text-left px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-md font-medium transition">
                Login
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AvatarMenu;
