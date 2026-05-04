/*
Root React router. It maps URLs to pages and wraps private pages with authentication checks so users only see screens they are allowed to access.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

import React from "react";
import { HashRouter as Router, Routes, Route } from "react-router-dom";

// ===== Pages =====
import Register from "./pages/Register";
import Login from "./pages/Login";
import Home from "./pages/Home";
import AdminLogin from "./pages/AdminLogin";
import AdminDashboard from "./pages/AdminDashboard";
import Chatbot from "./pages/Chatbot"; // <- import chatbot page
import Dashboard from "./pages/Dashboard";
import ScholarshipFinder from "./pages/ScholarshipFinder";
import BehaviorAnalysis from "./pages/BehaviorAnalysis";
import CareerPathPage from "./pages/CareerPathPage";
import ProtectedRoute from "./components/ProtectedRoute";
import ProtectedLayout from "./components/ProtectedLayout";

const App = () => {
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
              <ProtectedLayout>
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              </ProtectedLayout>
            } 
          />

          {/* ===== Authentication ===== */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route 
            path="/admin" 
            element={
              <ProtectedLayout>
                <ProtectedRoute>
                  <AdminDashboard />
                </ProtectedRoute>
              </ProtectedLayout>
            } 
          />

          {/* ===== Career Path ===== */}
          <Route 
            path="/form" 
            element={
              <ProtectedLayout>
                <ProtectedRoute>
                  <CareerPathPage />
                </ProtectedRoute>
              </ProtectedLayout>
            } 
          />
          {/* ===== Chatbot Page ===== */}
          <Route 
            path="/chatbot" 
            element={
              <ProtectedLayout>
                <ProtectedRoute>
                  <Chatbot />
                </ProtectedRoute>
              </ProtectedLayout>
            } 
          />

          <Route 
            path="/scholarships" 
            element={
              <ProtectedLayout>
                <ProtectedRoute>
                  <ScholarshipFinder />
                </ProtectedRoute>
              </ProtectedLayout>
            } 
          />

          <Route 
            path="/behavior" 
            element={
              <ProtectedLayout>
                <ProtectedRoute>
                  <BehaviorAnalysis />
                </ProtectedRoute>
              </ProtectedLayout>
            } 
          />

          <Route
            path="/behavior-career-result"
            element={
              <ProtectedLayout>
                <ProtectedRoute>
                  <CareerPathPage />
                </ProtectedRoute>
              </ProtectedLayout>
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
