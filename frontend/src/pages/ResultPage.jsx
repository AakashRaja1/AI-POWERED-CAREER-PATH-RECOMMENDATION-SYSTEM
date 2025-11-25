import React from "react";
import ResultCard from "../assets/components/ResultCard";

const ResultPage = ({ result }) => {
  return (
    <div className="relative min-h-screen bg-linear-to-b from-neutral-950 via-neutral-900 to-black text-gray-100 font-poppins flex flex-col items-center justify-center px-6 py-16 overflow-hidden">
      {/* Background AI Theme */}
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center opacity-10"></div>
      <div className="absolute inset-0 bg-linear-to-b from-black/80 via-neutral-900/70 to-black"></div>

      {/* Header */}
      <h1 className="relative z-10 text-4xl sm:text-5xl font-extrabold text-center mb-10 text-blue-400 drop-shadow-[0_0_8px_rgba(59,130,246,0.6)] animate-fadeIn">
        Your AI Career Recommendation
      </h1>

      {/* Result Section */}
      <div className="relative z-10 w-full max-w-5xl space-y-8 animate-slideUp">
        {result ? (
          <>
            {/* Main Result Card */}
            <div className="bg-neutral-900/70 backdrop-blur-md border border-neutral-700 rounded-2xl p-8 shadow-lg shadow-black/40 hover:shadow-blue-500/20 transition-all duration-300 hover:scale-[1.02]">
              <ResultCard
                result={result}
                onBack={() => (window.location.hash = "#/form")}
              />
            </div>

            {/* Detailed Info Boxes */}
            {result.details && Array.isArray(result.details) && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                {result.details.map((item, i) => (
                  <div
                    key={i}
                    className="bg-neutral-800/60 border border-neutral-700 rounded-2xl p-6 text-center shadow-md shadow-black/30 hover:shadow-blue-500/20 transition-all duration-300 hover:scale-[1.03]"
                  >
                    <h3 className="text-xl font-semibold text-blue-400 mb-3 drop-shadow">
                      {item.title || `Detail ${i + 1}`}
                    </h3>
                    <p className="text-gray-300">{item.description || item}</p>
                  </div>
                ))}
              </div>
            )}
          </>
        ) : (
          <div className="relative z-10 text-center bg-neutral-900/70 border border-neutral-700 backdrop-blur-md p-10 rounded-2xl shadow-lg shadow-black/40 max-w-xl mx-auto animate-fadeIn">
            <p className="text-2xl mb-6 text-gray-200">
              No result found. Please go back and submit the form.
            </p>
            <button
              onClick={() => (window.location.hash = "#/form")}
              className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30"
            >
              🔙 Go to Career Form
            </button>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="absolute bottom-4 text-gray-500 text-sm tracking-wide">
        Powered by{" "}
        <span className="text-blue-400 font-semibold">AI CareerPath</span>
      </div>
    </div>
  );
};

export default ResultPage;
