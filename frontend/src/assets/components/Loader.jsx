import React from "react";

const Loader = () => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex flex-col items-center justify-center z-50">
      <div className="w-24 h-24 border-8 border-dashed rounded-full animate-spin border-blue-500"></div>
      <p className="text-white text-xl mt-4">Predicting your career path...</p>
    </div>
  );
};

export default Loader;
