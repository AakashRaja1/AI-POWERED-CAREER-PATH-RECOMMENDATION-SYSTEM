import React, { useState } from "react";

const ResumeUploadForm = ({ onSubmit, loading }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onSubmit(file);
    } else {
      alert("Please select a file to upload.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label
          htmlFor="resume-upload"
          className="block text-sm font-medium text-gray-300 mb-2"
        >
          Upload your Resume (PDF only)
        </label>
        <input
          id="resume-upload"
          name="resume"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-500 file:text-white hover:file:bg-blue-600"
        />
      </div>
      <div>
        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-500"
        >
          {loading ? "Uploading..." : "Get Prediction"}
        </button>
      </div>
    </form>
  );
};

export default ResumeUploadForm;
