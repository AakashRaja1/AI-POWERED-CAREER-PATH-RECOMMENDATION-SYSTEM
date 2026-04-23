import React, { useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const BehaviorCareerResult = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const payload = useMemo(() => {
    if (location.state?.recommendation) {
      return location.state;
    }

    try {
      const stored = localStorage.getItem("behavior_career_result");
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  }, [location.state]);

  const recommendation = payload?.recommendation || null;
  const generatedAt = payload?.generated_at ? new Date(payload.generated_at).toLocaleString() : "";

  return (
    <div className="relative min-h-screen overflow-hidden bg-linear-to-br from-slate-950 via-slate-900 to-indigo-950 text-white">
      <div className="absolute inset-0 opacity-40">
        <div className="absolute -left-32 top-10 h-72 w-72 rounded-full bg-cyan-500 blur-3xl" />
        <div className="absolute -right-24 top-28 h-96 w-96 rounded-full bg-fuchsia-500 blur-3xl" />
        <div className="absolute bottom-0 left-1/2 h-80 w-80 -translate-x-1/2 rounded-full bg-emerald-500 blur-3xl" />
      </div>

      <div className="relative mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">
              Career Recommendation Result
            </p>
            <h1 className="mt-3 text-3xl font-black leading-tight sm:text-4xl lg:text-5xl">
              Personality-Based Career Recommendation
            </h1>
            {generatedAt && <p className="mt-2 text-sm text-slate-300">Generated: {generatedAt}</p>}
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={() => navigate("/behavior")}
              className="rounded-xl border border-white/20 bg-black/20 px-4 py-2 text-sm font-semibold text-white transition hover:border-white/40"
            >
              Back to behavior analysis
            </button>
            <button
              type="button"
              onClick={() => window.print()}
              className="rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:scale-[1.01]"
            >
              Print report
            </button>
          </div>
        </div>

        {!recommendation ? (
          <div className="rounded-3xl border border-white/10 bg-white/8 p-8 text-center backdrop-blur-xl">
            <p className="text-lg font-semibold text-white">No behavior-based recommendation found.</p>
            <p className="mt-2 text-sm text-slate-300">Run personality analysis and submit the questionnaire first.</p>
            <button
              type="button"
              onClick={() => navigate("/behavior")}
              className="mt-6 rounded-xl bg-linear-to-r from-cyan-500 to-fuchsia-500 px-5 py-3 text-sm font-bold text-white"
            >
              Go to behavior analysis
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="rounded-3xl border border-emerald-400/20 bg-emerald-400/10 p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-200">Best fit career path</p>
              <h2 className="mt-2 text-3xl font-black text-white">{recommendation.career_path || "Career recommendation"}</h2>
              {typeof recommendation.confidence !== "undefined" && (
                <p className="mt-2 text-sm text-slate-200">Confidence: {Number(recommendation.confidence).toFixed(2)}</p>
              )}
            </div>

            {recommendation.rationale && (
              <div className="rounded-3xl border border-white/10 bg-white/8 p-6 backdrop-blur-xl">
                <h3 className="text-xl font-bold text-white">Why this fit works</h3>
                <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-200">{recommendation.rationale}</p>
              </div>
            )}

            <div className="grid gap-6 lg:grid-cols-2">
              <div className="rounded-3xl border border-white/10 bg-white/8 p-6 backdrop-blur-xl">
                <h3 className="text-xl font-bold text-white">Best fit roles</h3>
                {Array.isArray(recommendation.best_fit_roles) && recommendation.best_fit_roles.length > 0 ? (
                  <ul className="mt-4 space-y-2 text-sm text-slate-200">
                    {recommendation.best_fit_roles.map((role) => (
                      <li key={role} className="rounded-xl bg-black/20 px-3 py-2">
                        {role}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="mt-3 text-sm text-slate-300">No role suggestions provided.</p>
                )}
              </div>

              <div className="rounded-3xl border border-white/10 bg-white/8 p-6 backdrop-blur-xl">
                <h3 className="text-xl font-bold text-white">Skills to build</h3>
                {Array.isArray(recommendation.skills_to_build) && recommendation.skills_to_build.length > 0 ? (
                  <ul className="mt-4 space-y-2 text-sm text-slate-200">
                    {recommendation.skills_to_build.map((skill) => (
                      <li key={skill} className="rounded-xl bg-black/20 px-3 py-2">
                        {skill}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="mt-3 text-sm text-slate-300">No specific skill plan provided.</p>
                )}
              </div>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/8 p-6 backdrop-blur-xl">
              <h3 className="text-xl font-bold text-white">Roadmap</h3>
              {Array.isArray(recommendation.roadmap) && recommendation.roadmap.length > 0 ? (
                <ol className="mt-4 space-y-2 text-sm text-slate-200">
                  {recommendation.roadmap.map((step, index) => (
                    <li key={`${step}-${index}`} className="rounded-xl bg-black/20 px-3 py-2">
                      {index + 1}. {step}
                    </li>
                  ))}
                </ol>
              ) : (
                <p className="mt-3 text-sm text-slate-300">No roadmap steps provided.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BehaviorCareerResult;