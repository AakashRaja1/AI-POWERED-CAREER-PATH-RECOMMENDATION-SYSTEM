import React, { useState } from "react";
import CareerForm from "../assets/components/CareerForm";
import ResumeUploadForm from "../assets/components/ResumeUploadForm"; // Import the new component
import ResultPage from "./ResultPage";

const CareerFormPage = ({ setResult }) => {
  const [loading, setLoading] = useState(false);
  const [formType, setFormType] = useState("form"); // 'form' or 'resume'

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    const token = localStorage.getItem("token");
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error details:", errorText);
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      setResult(data);
      window.location.hash = "#/result";
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("Failed to get prediction. Please check the backend or input data.");
    } finally {
      setLoading(false);
    }
  };

  const handleResumeSubmit = async (file) => {
    setLoading(true);
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict-resume", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error details:", errorText);
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      setResult(data);
      window.location.hash = "#/result";
    } catch (error) {
      console.error("Resume prediction failed:", error);
      alert("Failed to get prediction from resume. Please check the file or backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-linear-to-b from-neutral-950 via-neutral-900 to-black text-gray-100 font-poppins flex flex-col items-center justify-center overflow-hidden">
      {/* Background AI Effect */}
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center opacity-10"></div>
      <div className="absolute inset-0 bg-linear-to-b from-black/80 via-neutral-900/70 to-black"></div>

      {/* Page Title */}
      <h1 className="relative z-10 text-4xl sm:text-5xl font-extrabold mb-8 text-center text-blue-400 drop-shadow-[0_0_8px_rgba(59,130,246,0.6)] animate-fadeIn">
        AI Career Path Finder
      </h1>

      {/* Form Section */}
      <div className="relative z-10 w-full max-w-3xl bg-neutral-900/70 backdrop-blur-md border border-neutral-700 rounded-2xl p-8 shadow-xl shadow-black/40 animate-slideUp">
        {/* Toggle Switch */}
        <div className="flex justify-center mb-6">
          <div className="flex items-center bg-neutral-800 rounded-full p-1">
            <button
              onClick={() => setFormType("form")}
              className={`px-4 py-2 text-sm font-semibold rounded-full transition-colors ${
                formType === "form"
                  ? "bg-blue-600 text-white"
                  : "bg-transparent text-gray-400 hover:bg-neutral-700"
              }`}
            >
              Fill Form
            </button>
            <button
              onClick={() => setFormType("resume")}
              className={`px-4 py-2 text-sm font-semibold rounded-full transition-colors ${
                formType === "resume"
                  ? "bg-blue-600 text-white"
                  : "bg-transparent text-gray-400 hover:bg-neutral-700"
              }`}
            >
              Upload Resume
            </button>
          </div>
        </div>

        {formType === "form" ? (
          <CareerForm onSubmit={handleFormSubmit} loading={loading} />
        ) : (
          <ResumeUploadForm onSubmit={handleResumeSubmit} loading={loading} />
        )}

        {loading && (
          <p className="text-blue-400 font-semibold mt-6 text-center animate-pulse">
            ⏳ Predicting your career path...
          </p>
        )}
      </div>

      {/* Footer or Background Detail */}
      <div className="absolute bottom-4 text-gray-500 text-sm tracking-wide">
        Empowered by{" "}
        <span className="text-blue-400 font-semibold">AI Intelligence</span>
      </div>
    </div>
  );
};

export default CareerFormPage;
