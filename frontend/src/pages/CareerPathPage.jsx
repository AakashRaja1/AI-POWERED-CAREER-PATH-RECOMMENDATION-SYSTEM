/*
Career path form and result page. It combines questionnaire answers with saved personality results to generate a personalized career path.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { postWithFallback } from "../api/client";
import {
  getCurrentUserEmail,
  loadPersonalityAnalysis,
  persistCareerRecommendation,
  persistPersonalityAnalysis,
} from "../utils/personalityStorage";

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
  const location = useLocation();
  const [behavior, setBehavior] = useState(location.state?.behavior || null);
  const [showTest, setShowTest] = useState(Boolean(location.state?.autoStart));
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [recommendation, setRecommendation] = useState(null);

  useEffect(() => {
    const userEmail = getCurrentUserEmail();

    try {
      const latestBehavior = location.state?.behavior || loadPersonalityAnalysis(userEmail);
      if (latestBehavior) {
        setBehavior(latestBehavior);
        if (userEmail) {
          persistPersonalityAnalysis(userEmail, latestBehavior);
        }
        setShowTest(true);
      } else {
        setBehavior(null);
        setShowTest(Boolean(location.state?.autoStart));
      }
    } catch (e) {
      setBehavior(null);
    }
  }, [location.state]);

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
      const currentEmail = getCurrentUserEmail();
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
      const resultPayload = {
        recommendation: data.recommendation,
        personality_score: behavior,
        questionnaire_responses: payload.questionnaire_responses,
        generated_at: new Date().toISOString(),
      };

      localStorage.setItem("behavior_career_result", JSON.stringify(resultPayload));
      if (currentEmail) {
        persistCareerRecommendation(currentEmail, resultPayload);
      }
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white py-12 px-4">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-linear-to-br from-blue-200/50 to-transparent blur-3xl" />
        <div className="absolute top-1/4 -right-32 w-80 h-80 rounded-full bg-linear-to-bl from-violet-200/50 to-transparent blur-3xl" />
        <div className="absolute -bottom-40 left-1/2 w-96 h-96 rounded-full bg-linear-to-tr from-emerald-200/50 to-transparent blur-3xl" />
      </div>

      <div className="relative max-w-6xl mx-auto">
        <header className="mb-8 flex items-center justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold bg-linear-to-r from-blue-600 via-cyan-600 to-teal-600 bg-clip-text text-transparent">Career Path — Based on Behavior Analysis</h1>
            <p className="mt-2 text-gray-600">Combine your personality result with a short assessment to get targeted career recommendations and a clear roadmap.</p>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={() => navigate("/behavior")} className="px-4 py-2 rounded-lg bg-gray-200 text-gray-900 hover:bg-gray-300 font-medium transition">Back to Behavior</button>
            <button onClick={() => { try { localStorage.setItem("behavior_analysis_result", JSON.stringify(behavior || {})); } catch(e){}; setShowTest(true); }} className="px-4 py-2 rounded-lg bg-linear-to-r from-blue-500 to-cyan-500 text-white font-semibold shadow-lg hover:shadow-xl transition">Use Latest Personality Traits</button>
          </div>
        </header>

        {!behavior ? (
          <div className="rounded-2xl border-2 border-yellow-300 bg-linear-to-r from-yellow-50 to-orange-50 p-8 text-center shadow-lg">
            <div className="text-2xl font-bold text-yellow-600 mb-3">⚠️ Behavior Analysis Required</div>
            <p className="text-yellow-700 mb-6 max-w-2xl mx-auto">
              The Career Path module requires you to complete a Behavior Analysis first. Upload a video to analyze your personality traits and get more accurate career recommendations.
            </p>
            <button 
              onClick={() => navigate("/behavior")}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-linear-to-r from-yellow-500 to-orange-500 text-white font-bold hover:shadow-lg transition"
            >
              🎬 Go to Behavior Analysis
            </button>
          </div>
        ) : (
          <div className="grid gap-8 lg:grid-cols-3">
            <aside className="lg:col-span-1">
              <div className="rounded-2xl bg-white border border-blue-200 p-6 shadow-lg">
                <h2 className="text-lg font-semibold text-gray-900">Behavior Summary</h2>
                <p className="mt-2 text-sm text-gray-600">Quick view of your Big Five and visual/audio engagement metrics.</p>

                <div className="mt-4 space-y-4">
                  {behavior.traits && (
                    <div className="space-y-3">
                      {Object.entries(behavior.traits).map(([k, v]) => {
                        const val = Number(v || 0);
                        return (
                          <div key={k}>
                            <div className="flex items-center justify-between text-sm text-gray-700">
                              <div className="font-medium text-gray-900">{k.charAt(0).toUpperCase() + k.slice(1)}</div>
                              <div className="text-xs font-semibold">{val.toFixed(2)}</div>
                            </div>
                            <div className="w-full h-2 bg-gray-200 rounded mt-2">
                              <div className="h-2 rounded bg-linear-to-r from-blue-500 to-cyan-500" style={{ width: `${Math.max(0, Math.min(1, val)) * 100}%` }} />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {behavior.behavior_analysis && (
                    <div className="grid gap-2">
                      <div className="text-xs text-gray-600">Presence: <span className="font-medium text-gray-900">{behavior.behavior_analysis.frame_analysis?.presence_quality || "N/A"}</span></div>
                      <div className="text-xs text-gray-600">Face detection: <span className="font-medium text-gray-900">{typeof behavior.behavior_analysis.frame_analysis?.face_detection_rate !== "undefined" ? `${Math.round(behavior.behavior_analysis.frame_analysis.face_detection_rate * 100)}%` : "N/A"}</span></div>
                      <div className="text-xs text-gray-600">Smile rate: <span className="font-medium text-gray-900">{typeof behavior.behavior_analysis.frame_analysis?.expression_smile_rate !== "undefined" ? `${Math.round(behavior.behavior_analysis.frame_analysis.expression_smile_rate * 100)}%` : "N/A"}</span></div>
                      <div className="text-xs text-gray-600">Reliability: <span className="font-medium text-gray-900">{behavior.behavior_analysis.reliability_score ?? "N/A"}</span></div>
                    </div>
                  )}

                  {behavior.behavior_analysis?.behavior_summary && (
                    <div className="mt-3 rounded-lg bg-blue-50 border border-blue-200 p-3 text-sm text-gray-700">{behavior.behavior_analysis.behavior_summary}</div>
                  )}
                </div>
              </div>
            </aside>

            <main className="lg:col-span-2">
              <div className="rounded-2xl bg-white border border-blue-200 p-6 shadow-lg">
                <h3 className="text-lg font-semibold text-gray-900">Assessment</h3>
                <p className="mt-1 text-sm text-gray-600">Answer the short assessment below (all fields required) — we will combine these with your behavior analysis.</p>

                {!showTest ? (
                  <div className="mt-6 flex items-center gap-3">
                    <button onClick={() => setShowTest(true)} className="px-4 py-2 bg-linear-to-r from-blue-500 to-cyan-500 text-white rounded font-semibold shadow-lg hover:shadow-xl transition">Start Test</button>
                    <button onClick={() => { localStorage.removeItem("behavior_career_result"); setRecommendation(null); }} className="px-4 py-2 bg-gray-200 text-gray-900 rounded font-medium hover:bg-gray-300 transition">Clear results</button>
                  </div>
                ) : (
                  <form onSubmit={handleSubmit} className="mt-6 space-y-6">
                    <div className="grid gap-4 md:grid-cols-2">
                      {CAREER_FORM_QUESTIONS.map((q) => (
                        <div key={q.id} className="rounded-lg p-4 bg-blue-50 border border-blue-200 shadow-sm">
                          <label className="block text-sm font-medium text-gray-900 mb-3">{q.label}</label>
                          {q.type === "mcq" ? (
                            <div className="grid gap-2 sm:grid-cols-2">
                              {q.options.map((opt) => (
                                <button
                                  type="button"
                                  key={opt}
                                  onClick={() => handleChange(q.id, opt)}
                                  className={`text-left rounded-lg px-3 py-2 transition text-sm font-medium ${answers[q.id] === opt ? "bg-linear-to-r from-blue-500 to-cyan-500 text-white shadow-lg" : "bg-white text-gray-700 hover:bg-blue-100 border border-blue-200"}`}
                                >
                                  {opt}
                                </button>
                              ))}
                            </div>
                          ) : (
                            <input value={answers[q.id] || ""} onChange={(e) => handleChange(q.id, e.target.value)} placeholder={q.label} className="w-full rounded-lg px-3 py-2 bg-white border border-blue-200 text-gray-900 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-200" />
                          )}
                        </div>
                      ))}
                    </div>

                    {error && <div className="text-sm text-red-600 font-medium bg-red-50 border border-red-200 rounded-lg p-3">{error}</div>}

                    <div className="flex items-center gap-3">
                      <button type="submit" disabled={loading} className="px-6 py-3 rounded-lg bg-linear-to-r from-emerald-500 to-teal-500 text-white font-semibold shadow-lg hover:shadow-xl transition disabled:opacity-60">{loading ? "Submitting..." : "Submit & Get Recommendations"}</button>
                      <button type="button" onClick={() => setShowTest(false)} className="px-4 py-2 bg-gray-200 text-gray-900 rounded font-medium hover:bg-gray-300 transition">Cancel</button>
                    </div>
                  </form>
                )}

                {recommendation && (
                  <div className="mt-8 overflow-hidden rounded-3xl border border-blue-200 bg-white shadow-2xl">
                    <div className="border-b border-blue-200 bg-linear-to-r from-blue-50 to-cyan-50 px-6 py-5">
                      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                        <div className="max-w-3xl">
                          <div className="inline-flex rounded-full border border-blue-300 bg-linear-to-r from-blue-100 to-cyan-100 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.22em] text-blue-600">
                            Career Recommendation Report
                          </div>
                          <h4 className="mt-3 text-3xl font-black bg-linear-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent sm:text-4xl">
                            {recommendation.career_path}
                          </h4>
                          <p className="mt-3 text-sm leading-6 text-gray-700 sm:text-base">
                            {recommendation.rationale}
                          </p>
                        </div>

                        <div className="grid min-w-[190px] grid-cols-2 gap-3 lg:w-[220px]">
                          <div className="rounded-2xl border border-blue-200 bg-blue-50 p-4 text-center">
                            <div className="text-[11px] uppercase tracking-[0.2em] text-gray-600 font-semibold">Confidence</div>
                            <div className="mt-2 text-2xl font-extrabold text-blue-600">
                              {Number(recommendation.confidence ?? 0).toFixed(2)}
                            </div>
                          </div>
                          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-center">
                            <div className="text-[11px] uppercase tracking-[0.2em] text-gray-600 font-semibold">Status</div>
                            <div className="mt-2 text-sm font-semibold text-emerald-600">Ready</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="grid gap-5 px-6 py-6 lg:grid-cols-[1.1fr_0.9fr]">
                      <section className="rounded-2xl border border-blue-200 bg-blue-50 p-5">
                        <div className="flex items-center justify-between gap-3">
                          <h5 className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">Top 3 Career Matches</h5>
                          <span className="rounded-full bg-blue-100 px-3 py-1 text-xs text-blue-700 font-semibold">Best fit roles</span>
                        </div>

                        <div className="mt-4 space-y-3">
                          {Array.isArray(recommendation.best_fit_roles) && recommendation.best_fit_roles.length > 0 ? (
                            recommendation.best_fit_roles.slice(0, 3).map((role, index) => (
                              <div key={role} className="flex items-center gap-3 rounded-2xl border border-blue-200 bg-white px-4 py-3 shadow-sm hover:shadow-md transition">
                                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-linear-to-r from-blue-500 to-cyan-500 text-sm font-black text-white">
                                  {index + 1}
                                </div>
                                <div>
                                  <div className="text-sm font-semibold text-gray-900">{role}</div>
                                  <div className="text-xs text-gray-500">Matched from behavior + questionnaire signals</div>
                                </div>
                              </div>
                            ))
                          ) : (
                            <div className="rounded-2xl border border-blue-200 bg-white px-4 py-3 text-sm text-gray-600">
                              No ranked roles returned yet.
                            </div>
                          )}
                        </div>
                      </section>

                      <section className="rounded-2xl border border-fuchsia-200 bg-fuchsia-50 p-5">
                        <h5 className="text-sm font-semibold uppercase tracking-[0.2em] text-fuchsia-600">Skills To Build</h5>
                        <div className="mt-4 flex flex-wrap gap-2">
                          {Array.isArray(recommendation.skills_to_build) && recommendation.skills_to_build.length > 0 ? (
                            recommendation.skills_to_build.map((skill) => (
                              <span key={skill} className="rounded-full border border-fuchsia-200 bg-white px-3 py-2 text-xs text-fuchsia-700 font-medium">
                                {skill}
                              </span>
                            ))
                          ) : (
                            <span className="text-sm text-gray-600">No skills returned.</span>
                          )}
                        </div>

                        <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
                          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-600">What to do next</div>
                          <p className="mt-2 text-sm leading-6 text-gray-700">
                            Follow the roadmap below and keep using the behavior result as your anchor for career decisions.
                          </p>
                        </div>
                      </section>
                    </div>

                    {Array.isArray(recommendation.roadmap) && recommendation.roadmap.length > 0 && (
                      <div className="border-t border-blue-200 px-6 py-6 bg-linear-to-br from-blue-50 to-cyan-50">
                        <h5 className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">Roadmap</h5>
                        <ol className="mt-4 space-y-3">
                          {recommendation.roadmap.map((step, i) => (
                            <li key={i} className="flex gap-4 rounded-2xl border border-blue-200 bg-white p-4 shadow-sm hover:shadow-md transition">
                              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-linear-to-r from-blue-500 to-cyan-500 text-sm font-bold text-white">
                                {i + 1}
                              </div>
                              <div className="pt-1 text-sm leading-6 text-gray-700">{step}</div>
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
