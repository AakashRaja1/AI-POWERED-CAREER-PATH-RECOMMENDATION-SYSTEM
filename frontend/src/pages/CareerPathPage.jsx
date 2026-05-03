import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { postWithFallback } from "../api/client";

const CAREER_FORM_QUESTIONS = [
  { id: "q1", type: "mcq", label: "Preferred work environment:", options: ["High pressure, fast-paced", "Moderate pressure", "Stable and predictable", "Flexible, low pressure"] },
  { id: "q2", type: "mcq", label: "Work style preference:", options: ["Team-heavy", "Balanced", "Mostly independent", "Fully independent"] },
  { id: "q3", type: "mcq", label: "Decision-making approach:", options: ["Quick decisions", "Balanced thinking", "Deep analysis", "Depend on others"] },
  { id: "q4", type: "mcq", label: "Risk tolerance:", options: ["High risk (startup/freelance)", "Moderate risk", "Low risk", "Very safe career"] },
  { id: "q5", type: "mcq", label: "Task preference:", options: ["Leading people", "Solving technical problems", "Helping others", "Managing/organizing"] },
  { id: "q6", type: "mcq", label: "Reaction to criticism:", options: ["Improve quickly", "Analyze calmly", "Ignore", "Feel discouraged"] },
  { id: "q7", type: "mcq", label: "Leadership tendency:", options: ["Naturally lead", "Lead when needed", "Support role", "Avoid leadership"] },
  { id: "q8", type: "mcq", label: "Communication comfort:", options: ["Public speaking", "Group discussion", "Written communication", "One-on-one"] },
  { id: "q9", type: "mcq", label: "Motivation driver:", options: ["Money & growth", "Balance", "Stability", "Purpose/helping others"] },
  { id: "q10", type: "mcq", label: "Consistency level:", options: ["Very consistent", "Mostly consistent", "Inconsistent", "Very inconsistent"] },
  { id: "q11", type: "short", label: "Matric Percentage (%)" },
  { id: "q12", type: "short", label: "FSC / Intermediate Percentage (%)" },
  { id: "q13", type: "mcq", label: "FSC Group:", options: ["Pre-Medical", "Pre-Engineering", "ICS", "Commerce", "Arts"] },
  { id: "q14", type: "mcq", label: "Do you have any skills?", options: ["Programming", "Design", "Writing/Content", "Video/Media", "None"] },
  { id: "q15", type: "mcq", label: "Skill proficiency level:", options: ["Beginner", "Intermediate", "Advanced"] },
  { id: "q16", type: "mcq", label: "Have you done any projects?", options: ["Yes (personal/academic)", "Yes (freelance/internship)", "No"] },
  { id: "q17", type: "mcq", label: "What do you enjoy most?", options: ["Problem solving", "People interaction", "Creativity/design", "Organizing systems"] },
  { id: "q18", type: "short", label: "Your hobbies (write briefly)" },
  { id: "q19", type: "mcq", label: "Financial situation:", options: ["Can study long-term", "Need income soon", "Need immediate earning"] },
  { id: "q20", type: "mcq", label: "Willingness to relocate:", options: ["Anywhere", "Within country", "Not willing"] },
];

export default function CareerPathPage() {
  const navigate = useNavigate();
  const [behavior, setBehavior] = useState(null);
  const [showTest, setShowTest] = useState(false);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [recommendation, setRecommendation] = useState(null);

  useEffect(() => {
    const userEmail = localStorage.getItem("userEmail");
    
    try {
      // Only load behavior analysis specific to the current user's email
      // This prevents showing previous user's data to new users
      if (userEmail) {
        const emailKey = `behavior_analysis_${userEmail}`;
        const raw = localStorage.getItem(emailKey);
        if (raw) {
          const parsed = JSON.parse(raw);
          setBehavior(parsed);
        } else {
          setBehavior(null);
        }
      } else {
        // No email = not logged in properly, clear behavior
        setBehavior(null);
      }
    } catch (e) {
      setBehavior(null);
    }
  }, []);

  const handleChange = (id, value) => {
    setAnswers((prev) => ({ ...prev, [id]: value }));
  };

  const validateRequired = () => {
    // Require all MCQ and short answers except optional hobbies maybe; follow user's spec: all questions required
    for (const q of CAREER_FORM_QUESTIONS) {
      const val = answers[q.id];
      if (typeof val === "undefined" || String(val).trim() === "") return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!behavior) {
      setError("Please run behavior analysis first.");
      return;
    }
    if (!validateRequired()) {
      setError("Please answer all questions.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        personality_score: behavior,
        questionnaire_responses: CAREER_FORM_QUESTIONS.reduce((acc, q) => {
          acc[q.label] = answers[q.id];
          return acc;
        }, {}),
        additional_notes: "",
      };

      const data = await postWithFallback("/personality/recommend-career", payload, { timeoutMs: 60000 });
      setRecommendation(data.recommendation || data.recommendation);
      // store for result page
      localStorage.setItem("behavior_career_result", JSON.stringify({ recommendation: data.recommendation, personality_score: behavior, questionnaire_responses: payload.questionnaire_responses, generated_at: new Date().toISOString() }));
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-indigo-900 to-slate-950 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 flex items-center justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-white">Career Path — Based on Behavior Analysis</h1>
            <p className="mt-2 text-slate-300">Combine your personality result with a short assessment to get targeted career recommendations and a clear roadmap.</p>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={() => navigate("/behavior")} className="px-4 py-2 rounded-lg bg-white/10 text-white hover:bg-white/20">Back to Behavior</button>
            <button onClick={() => { try { localStorage.setItem("behavior_analysis_result", JSON.stringify(behavior || {})); } catch(e){}; setShowTest(true); }} className="px-4 py-2 rounded-lg bg-linear-to-r from-cyan-400 to-fuchsia-500 text-slate-900 font-semibold shadow">Start Career Path Test</button>
          </div>
        </header>

        {!behavior ? (
          <div className="rounded-2xl border-2 border-yellow-500/40 bg-linear-to-r from-yellow-500/10 to-orange-500/10 p-8 text-center">
            <div className="text-2xl font-bold text-yellow-300 mb-3">⚠️ Behavior Analysis Required</div>
            <p className="text-yellow-200 mb-6 max-w-2xl mx-auto">
              The Career Path module requires you to complete a Behavior Analysis first. Upload a video to analyze your personality traits and get more accurate career recommendations.
            </p>
            <button 
              onClick={() => navigate("/behavior")}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-linear-to-r from-yellow-500 to-orange-500 text-slate-900 font-bold hover:shadow-lg transition"
            >
              🎬 Go to Behavior Analysis
            </button>
          </div>
        ) : (
          <div className="grid gap-8 lg:grid-cols-3">
            <aside className="lg:col-span-1">
              <div className="rounded-2xl bg-white/5 p-6 border border-white/10 shadow">
                <h2 className="text-lg font-semibold text-white">Behavior Summary</h2>
                <p className="mt-2 text-sm text-slate-300">Quick view of your Big Five and visual/audio engagement metrics.</p>

                <div className="mt-4 space-y-4">
                  {behavior.traits && (
                    <div className="space-y-3">
                      {Object.entries(behavior.traits).map(([k, v]) => {
                        const val = Number(v || 0);
                        return (
                          <div key={k}>
                            <div className="flex items-center justify-between text-sm text-slate-200">
                              <div className="font-medium">{k.charAt(0).toUpperCase() + k.slice(1)}</div>
                              <div className="text-xs">{val.toFixed(2)}</div>
                            </div>
                            <div className="w-full h-2 bg-white/10 rounded mt-2">
                              <div className="h-2 rounded bg-linear-to-r from-cyan-400 to-fuchsia-400" style={{ width: `${Math.max(0, Math.min(1, val)) * 100}%` }} />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {behavior.behavior_analysis && (
                    <div className="grid gap-2">
                      <div className="text-xs text-slate-300">Presence: <span className="font-medium text-white">{behavior.behavior_analysis.frame_analysis?.presence_quality || "N/A"}</span></div>
                      <div className="text-xs text-slate-300">Face detection: <span className="font-medium text-white">{typeof behavior.behavior_analysis.frame_analysis?.face_detection_rate !== "undefined" ? `${Math.round(behavior.behavior_analysis.frame_analysis.face_detection_rate * 100)}%` : "N/A"}</span></div>
                      <div className="text-xs text-slate-300">Smile rate: <span className="font-medium text-white">{typeof behavior.behavior_analysis.frame_analysis?.expression_smile_rate !== "undefined" ? `${Math.round(behavior.behavior_analysis.frame_analysis.expression_smile_rate * 100)}%` : "N/A"}</span></div>
                      <div className="text-xs text-slate-300">Reliability: <span className="font-medium text-white">{behavior.behavior_analysis.reliability_score ?? "N/A"}</span></div>
                    </div>
                  )}

                  {behavior.behavior_analysis?.behavior_summary && (
                    <div className="mt-3 rounded-lg bg-black/20 p-3 text-sm text-slate-200">{behavior.behavior_analysis.behavior_summary}</div>
                  )}
                </div>
              </div>
            </aside>

            <main className="lg:col-span-2">
              <div className="rounded-2xl bg-white/5 p-6 border border-white/10 shadow">
                <h3 className="text-lg font-semibold text-white">Assessment</h3>
                <p className="mt-1 text-sm text-slate-300">Answer the short assessment below (all fields required) — we will combine these with your behavior analysis.</p>

                {!showTest ? (
                  <div className="mt-6 flex items-center gap-3">
                    <button onClick={() => setShowTest(true)} className="px-4 py-2 bg-linear-to-r from-cyan-400 to-fuchsia-500 text-slate-900 rounded font-semibold shadow">Start Test</button>
                    <button onClick={() => { localStorage.removeItem("behavior_career_result"); setRecommendation(null); }} className="px-4 py-2 bg-white/10 text-white rounded">Clear results</button>
                  </div>
                ) : (
                  <form onSubmit={handleSubmit} className="mt-6 space-y-6">
                    <div className="grid gap-4 md:grid-cols-2">
                      {CAREER_FORM_QUESTIONS.map((q) => (
                        <div key={q.id} className="rounded-lg p-4 bg-black/10 border border-white/6">
                          <label className="block text-sm font-medium text-white mb-3">{q.label}</label>
                          {q.type === "mcq" ? (
                            <div className="grid gap-2 sm:grid-cols-2">
                              {q.options.map((opt) => (
                                <button
                                  type="button"
                                  key={opt}
                                  onClick={() => handleChange(q.id, opt)}
                                  className={`text-left rounded-lg px-3 py-2 transition ${answers[q.id] === opt ? "bg-linear-to-r from-cyan-500 to-fuchsia-500 text-slate-900" : "bg-white/5 text-slate-200 hover:bg-white/10"}`}
                                >
                                  {opt}
                                </button>
                              ))}
                            </div>
                          ) : (
                            <input value={answers[q.id] || ""} onChange={(e) => handleChange(q.id, e.target.value)} placeholder={q.label} className="w-full rounded-lg px-3 py-2 bg-white/5 text-white outline-none" />
                          )}
                        </div>
                      ))}
                    </div>

                    {error && <div className="text-sm text-red-400">{error}</div>}

                    <div className="flex items-center gap-3">
                      <button type="submit" disabled={loading} className="px-6 py-3 rounded-lg bg-emerald-500 text-white font-semibold shadow">{loading ? "Submitting..." : "Submit & Get Recommendations"}</button>
                      <button type="button" onClick={() => setShowTest(false)} className="px-4 py-2 bg-white/10 text-white rounded">Cancel</button>
                    </div>
                  </form>
                )}

                {recommendation && (
                  <div className="mt-8 overflow-hidden rounded-3xl border border-cyan-400/20 bg-linear-to-br from-slate-950 via-slate-900 to-indigo-950 shadow-2xl">
                    <div className="border-b border-white/10 bg-white/5 px-6 py-5">
                      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                        <div className="max-w-3xl">
                          <div className="inline-flex rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.22em] text-cyan-200">
                            Career Recommendation Report
                          </div>
                          <h4 className="mt-3 text-3xl font-black text-white sm:text-4xl">
                            {recommendation.career_path}
                          </h4>
                          <p className="mt-3 text-sm leading-6 text-slate-300 sm:text-base">
                            {recommendation.rationale}
                          </p>
                        </div>

                        <div className="grid min-w-[190px] grid-cols-2 gap-3 lg:w-[220px]">
                          <div className="rounded-2xl border border-white/10 bg-black/20 p-4 text-center">
                            <div className="text-[11px] uppercase tracking-[0.2em] text-slate-400">Confidence</div>
                            <div className="mt-2 text-2xl font-extrabold text-white">
                              {Number(recommendation.confidence ?? 0).toFixed(2)}
                            </div>
                          </div>
                          <div className="rounded-2xl border border-white/10 bg-black/20 p-4 text-center">
                            <div className="text-[11px] uppercase tracking-[0.2em] text-slate-400">Status</div>
                            <div className="mt-2 text-sm font-semibold text-emerald-300">Ready</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="grid gap-5 px-6 py-6 lg:grid-cols-[1.1fr_0.9fr]">
                      <section className="rounded-2xl border border-white/10 bg-white/5 p-5">
                        <div className="flex items-center justify-between gap-3">
                          <h5 className="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-200">Top 3 Career Matches</h5>
                          <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-200">Best fit roles</span>
                        </div>

                        <div className="mt-4 space-y-3">
                          {Array.isArray(recommendation.best_fit_roles) && recommendation.best_fit_roles.length > 0 ? (
                            recommendation.best_fit_roles.slice(0, 3).map((role, index) => (
                              <div key={role} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-black/20 px-4 py-3">
                                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-linear-to-r from-cyan-400 to-fuchsia-500 text-sm font-black text-slate-950">
                                  {index + 1}
                                </div>
                                <div>
                                  <div className="text-sm font-semibold text-white">{role}</div>
                                  <div className="text-xs text-slate-400">Matched from behavior + questionnaire signals</div>
                                </div>
                              </div>
                            ))
                          ) : (
                            <div className="rounded-2xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-slate-300">
                              No ranked roles returned yet.
                            </div>
                          )}
                        </div>
                      </section>

                      <section className="rounded-2xl border border-white/10 bg-white/5 p-5">
                        <h5 className="text-sm font-semibold uppercase tracking-[0.2em] text-fuchsia-200">Skills To Build</h5>
                        <div className="mt-4 flex flex-wrap gap-2">
                          {Array.isArray(recommendation.skills_to_build) && recommendation.skills_to_build.length > 0 ? (
                            recommendation.skills_to_build.map((skill) => (
                              <span key={skill} className="rounded-full border border-white/10 bg-black/20 px-3 py-2 text-xs text-slate-100">
                                {skill}
                              </span>
                            ))
                          ) : (
                            <span className="text-sm text-slate-300">No skills returned.</span>
                          )}
                        </div>

                        <div className="mt-6 rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-4">
                          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">What to do next</div>
                          <p className="mt-2 text-sm leading-6 text-slate-200">
                            Follow the roadmap below and keep using the behavior result as your anchor for career decisions.
                          </p>
                        </div>
                      </section>
                    </div>

                    {Array.isArray(recommendation.roadmap) && recommendation.roadmap.length > 0 && (
                      <div className="border-t border-white/10 px-6 py-6">
                        <h5 className="text-sm font-semibold uppercase tracking-[0.2em] text-amber-200">Roadmap</h5>
                        <ol className="mt-4 space-y-3">
                          {recommendation.roadmap.map((step, i) => (
                            <li key={i} className="flex gap-4 rounded-2xl border border-white/10 bg-black/20 p-4">
                              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white/10 text-sm font-bold text-white">
                                {i + 1}
                              </div>
                              <div className="pt-1 text-sm leading-6 text-slate-200">{step}</div>
                            </li>
                          ))}
                        </ol>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </main>
          </div>
        )}
      </div>
    </div>
  );
}
