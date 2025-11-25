import React, { useState } from "react";

export default function CareerForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    "Full Name": "",
    "Education Level": "",
    "Academic Performance": "",
    "Skills": "",
    "Certifications": "",
    "Do you prefer working with data, people, or ideas?": "",
    "How do you approach solving complex problems?": "",
    "Do you thrive better in a structured or flexible environment?": "",
    "Do you prefer working independently or in a team?": "",
    "Do you learn best through practice, observation, or theory?": "",
    "Interests": "",
    "Extra-Curricular Activities": "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(form);
      }}
      className="max-w-2xl w-full mx-auto mt-10 p-8 bg-linear-to-br from-neutral-900 to-neutral-800 border border-neutral-700 rounded-2xl shadow-2xl backdrop-blur-lg animate-fadeIn font-poppins"
    >
      <h2 className="text-center text-2xl sm:text-3xl font-bold text-blue-400 mb-6">
        Career Recommendation Form
      </h2>

      <div className="space-y-5">
        {Object.keys(form).map((key) => (
          <div key={key} className="flex flex-col">
            <label className="text-gray-300 font-semibold mb-2">
              {key}
            </label>
            <input
              name={key}
              value={form[key]}
              onChange={handleChange}
              placeholder={`Enter ${key}`}
              required
              className="w-full px-4 py-3 bg-neutral-950 text-gray-200 border border-neutral-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-300 hover:shadow-[0_0_10px_rgba(77,163,255,0.3)]"
            />
          </div>
        ))}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full mt-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-lg disabled:bg-gray-500"
      >
        {loading ? "Getting Recommendation..." : "🚀 Get Recommendation"}
      </button>
    </form>
  );
}
