import { useNavigate } from "react-router-dom";

export default function CareerPathDisabled() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white/10 backdrop-blur-xl rounded-3xl border border-white/20 p-8 text-center shadow-2xl">
        <div className="mb-6 text-6xl">🔒</div>
        
        <h1 className="text-3xl font-bold text-white mb-3">
          Career Path Feature
        </h1>
        
        <p className="text-lg text-slate-300 mb-6">
          Must get the behavior analysis for Career Path recommendation
        </p>
        
        <p className="text-sm text-slate-400 mb-8">
          Please complete the personality analysis first by uploading a video. This will help us provide you with personalized career recommendations.
        </p>
        
        <button
          onClick={() => navigate("/behavior")}
          className="w-full bg-linear-to-r from-cyan-500 to-fuchsia-500 text-white font-bold py-3 rounded-lg hover:shadow-lg transition-all duration-300"
        >
          Go to Behavior Analysis
        </button>
        
        <button
          onClick={() => navigate("/")}
          className="w-full mt-3 bg-white/10 text-white font-bold py-3 rounded-lg hover:bg-white/20 transition-all duration-300"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}
