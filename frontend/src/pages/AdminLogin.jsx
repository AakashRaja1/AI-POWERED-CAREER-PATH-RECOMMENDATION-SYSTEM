import React, { useState } from "react";

const AdminLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    console.log("Admin login attempt:", email);
    
    if (!email || !password) {
      alert("Please enter both email and password");
      return;
    }
    
    setLoading(true);
    
    try {
      console.log("Sending login request...");
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });
      
      console.log("Response status:", response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log("Login response:", data);
        
        if (data.is_admin) {
          localStorage.setItem("token", data.access_token);
          localStorage.setItem("isAdmin", "true");
          localStorage.setItem("userName", "Admin");
          alert("Admin login successful! Redirecting...");
          window.location.hash = "#/admin";
        } else {
          alert("This account is not an admin account. Please use regular login.");
        }
      } else {
        let errorMessage = "Invalid credentials. Please try again.";
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
          console.error("Login error:", errorData);
        } catch (parseError) {
          errorMessage = `Login failed with status ${response.status}`;
          console.error("Parse error:", parseError);
        }
        alert(`Login failed: ${errorMessage}`);
      }
    } catch (error) {
      console.error("Admin login error:", error);
      alert(`An error occurred during login: ${error.message}\n\nPlease check:\n1. Server is running on http://localhost:8000\n2. Your network connection\n3. Browser console for details`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-linear-to-b from-neutral-950 via-neutral-900 to-black text-gray-100 font-poppins flex items-center justify-center overflow-hidden px-4">
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center opacity-10"></div>
      <div className="absolute inset-0 bg-linear-to-b from-black/80 via-neutral-900/70 to-black"></div>

      <div className="relative z-10 w-full max-w-md bg-neutral-900/70 backdrop-blur-lg border border-neutral-700 rounded-2xl p-8 shadow-lg shadow-black/40">
        <h2 className="text-4xl font-extrabold mb-2 text-center text-red-400 drop-shadow-[0_0_8px_rgba(239,68,68,0.6)]">
          Admin Login
        </h2>
        <p className="text-center text-gray-400 text-sm mb-8">
          Access admin dashboard
        </p>
        <form onSubmit={handleAdminLogin} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-gray-400 font-medium mb-2">
              Admin Email
            </label>
            <input
              className="w-full bg-neutral-800/80 text-gray-100 p-3 rounded-xl border border-neutral-700 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all duration-300"
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="admin@careerpath.com"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-gray-400 font-medium mb-2">
              Password
            </label>
            <input
              className="w-full bg-neutral-800/80 text-gray-100 p-3 rounded-xl border border-neutral-700 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all duration-300"
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter admin password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-3 rounded-xl text-lg transition-all duration-300 transform hover:scale-[1.03] hover:shadow-lg hover:shadow-red-500/30 cursor-pointer ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            {loading ? "⏳ Logging in..." : "🔐 Login as Admin"}
          </button>
        </form>

        <p className="text-center text-gray-400 mt-6">
          <a href="#/" className="text-blue-400 hover:text-blue-500 font-medium transition">
            ← Back to Home
          </a>
        </p>
      </div>
    </div>
  );
};

export default AdminLogin;

