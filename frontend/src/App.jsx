import React, { useState } from "react";
import { HashRouter as Router, Routes, Route } from "react-router-dom";

// ===== Pages =====
import Register from "./pages/Register";
import Login from "./pages/Login";
import Home from "./pages/Home";
import CareerFormPage from "./pages/CareerFormPage";
import ResultPage from "./pages/ResultPage";
import AdminLogin from "./pages/AdminLogin";
import AdminDashboard from "./pages/AdminDashboard";
import Chatbot from "./pages/Chatbot"; // <- import chatbot page
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";

const App = () => {
  const [result, setResult] = useState(null);

  return (
    <Router>
      <div className="bg-white text-gray-900 font-poppins min-h-screen">
        <Routes>
          {/* ===== Home Page ===== */}
          <Route path="/" element={<Home />} />

          {/* ===== Dashboard ===== */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />

          {/* ===== Authentication ===== */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route 
            path="/admin" 
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            } 
          />

          {/* ===== Career Recommendation Flow (Protected) ===== */}
          <Route 
            path="/form" 
            element={
              <ProtectedRoute>
                <CareerFormPage setResult={setResult} />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/result" 
            element={
              <ProtectedRoute>
                <ResultPage result={result} />
              </ProtectedRoute>
            } 
          />

          {/* ===== Chatbot Page ===== */}
          <Route 
            path="/chatbot" 
            element={
              <ProtectedRoute>
                <Chatbot />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
