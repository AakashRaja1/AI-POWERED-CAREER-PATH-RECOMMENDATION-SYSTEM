import React, { useState } from "react";

const Login = ({ setLoggedIn = () => {} }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
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
      
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("userName", email); // keep consistent with Home.jsx
        if (data.is_admin) {
          localStorage.setItem("isAdmin", "true");
        } else {
          localStorage.removeItem("isAdmin");
        }
        setLoggedIn(true);
        window.location.hash = "#/";
      } else {
        let errorMessage = "Invalid credentials. Please try again.";
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (parseError) {
          errorMessage = `Login failed with status ${response.status}`;
        }
        console.error("Login failed:", errorMessage);
        alert(`Login failed: ${errorMessage}`);
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("An error occurred during login. Please check your network connection and make sure the server is running on http://localhost:8000");
    }
  };

  return (
    <div className="relative min-h-screen bg-linear-to-b from-neutral-950 via-neutral-900 to-black text-gray-100 font-poppins flex items-center justify-center overflow-hidden px-4">
      {/* Background AI Theme */}
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center opacity-10"></div>
      <div className="absolute inset-0 bg-linear-to-b from-black/80 via-neutral-900/70 to-black"></div>

      {/* Login Box */}
      <div className="relative z-10 w-full max-w-md bg-neutral-900/70 backdrop-blur-lg border border-neutral-700 rounded-2xl p-8 shadow-lg shadow-black/40 animate-fadeIn">
        <h2 className="text-4xl font-extrabold mb-8 text-center text-blue-400 drop-shadow-[0_0_8px_rgba(59,130,246,0.6)]">
          Welcome Back
        </h2>
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label
              htmlFor="email"
              className="block text-gray-400 font-medium mb-2"
            >
              Email
            </label>
            <input
              className="w-full bg-neutral-800/80 text-gray-100 p-3 rounded-xl border border-neutral-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all duration-300"
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
            />
          </div>
          <div>
            <label
              htmlFor="password"
              className="block text-gray-400 font-medium mb-2"
            >
              Password
            </label>
            <input
              className="w-full bg-neutral-800/80 text-gray-100 p-3 rounded-xl border border-neutral-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all duration-300"
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 rounded-xl text-lg transition-all duration-300 transform hover:scale-[1.03] hover:shadow-lg hover:shadow-blue-500/30"
          >
            🔐 Login
          </button>
        </form>

        <p className="text-center text-gray-400 mt-6">
          Don’t have an account?{" "}
          <a
            href="#/register"
            className="text-blue-400 hover:text-blue-500 font-medium transition"
          >
            Register
          </a>
        </p>
      </div>

      {/* Footer */}
      <div className="absolute bottom-4 text-gray-500 text-sm tracking-wide">
        Secured by{" "}
        <span className="text-blue-400 font-semibold">AI CareerPath</span>
      </div>
    </div>
  );
};

export default Login;
