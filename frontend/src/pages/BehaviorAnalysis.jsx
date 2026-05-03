import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

const TRAIT_LABELS = [
  ["openness", "Openness"],
  ["conscientiousness", "Conscientiousness"],
  ["extraversion", "Extraversion"],
  ["agreeableness", "Agreeableness"],
  ["neuroticism", "Neuroticism"],
];

const API_URL = import.meta.env.VITE_PERSONALITY_API_URL || "http://127.0.0.1:8000/personality/predict";
const toTitle = (key) =>
  String(key)
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

const BehaviorAnalysis = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0] || null;
    setError("");
    setResult(null);
    

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl("");
    }

    if (!selectedFile) {
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError("Select a video first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const contentType = response.headers.get("content-type") || "";
        const message = contentType.includes("application/json")
          ? (await response.json())?.detail
          : await response.text();
        throw new Error(message || "Behavior prediction failed.");
      }

      const data = await response.json();
      const normalized = data?.traits
        ? data
        : {
            traits: data || {},
            direct_traits: {},
            derived_scores: {},
            score_levels: {},
            meta: {},
          };
      setResult(normalized);
      try {
        // Save with email-based key only to prevent data mixing between users
        const userEmail = localStorage.getItem("userEmail");
        if (userEmail) {
          const emailKey = `behavior_analysis_${userEmail}`;
          localStorage.setItem(emailKey, JSON.stringify(normalized));
          localStorage.setItem("behavior_analysis_timestamp_" + userEmail, new Date().toISOString());
        }
      } catch (e) {
        // ignore storage errors
      }
    } catch (predictionError) {
      setError(predictionError.message || "Unable to analyze the file.");
    } finally {
      setLoading(false);
    }
  };

  

  return (
    <div className="relative min-h-screen overflow-hidden bg-linear-to-br from-slate-950 via-slate-900 to-indigo-950 text-white">
      <div className="absolute inset-0 opacity-40">
        <div className="absolute -left-32 top-10 h-72 w-72 rounded-full bg-cyan-500 blur-3xl" />
        <div className="absolute -right-24 top-28 h-96 w-96 rounded-full bg-fuchsia-500 blur-3xl" />
        <div className="absolute bottom-0 left-1/2 h-80 w-80 -translate-x-1/2 rounded-full bg-amber-500 blur-3xl" />
      </div>

      <div className="relative mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <p className="mb-3 inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-cyan-200">
            Deep Learning Behavior Analysis
          </p>
          <h1 className="text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">
            Upload a video and get rich personality insights.
          </h1>
          <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-300 sm:text-base">
            This page calls the integrated FastAPI personality module backed by the trained CNN behavior model.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
          <form onSubmit={handleSubmit} className="rounded-3xl border border-white/10 bg-white/8 p-6 shadow-2xl backdrop-blur-xl sm:p-8">
            <div className="mb-6 rounded-2xl border border-dashed border-white/15 bg-black/20 p-6">
              <label className="block cursor-pointer text-center">
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleFileChange}
                  className="hidden"
                />
                <div className="space-y-2">
                  <div className="text-lg font-semibold text-white">Choose a video for personality analysis</div>
                  <div className="text-sm text-slate-300">MP4, MOV, WEBM, AVI, MKV (max 10 min)</div>
                </div>
                <div className="mt-5 inline-flex rounded-full bg-white px-5 py-3 text-sm font-semibold text-slate-900 transition hover:scale-[1.02]">
                  Browse files
                </div>
              </label>
            </div>

            {file && (
              <div className="mb-6 rounded-2xl bg-white/8 p-4 text-sm text-slate-200">
                <p className="font-semibold text-white">Selected file</p>
                <p className="mt-1 break-all">{file.name}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="inline-flex w-full items-center justify-center rounded-2xl bg-linear-to-r from-cyan-500 to-fuchsia-500 px-6 py-4 text-base font-bold text-white shadow-lg transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Analyzing..." : "Analyze Personality"}
            </button>

            {error && (
              <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
                {error}
              </p>
            )}

            <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-4 text-xs leading-5 text-slate-300">
              <p className="font-semibold text-white">FastAPI service</p>
              <p className="mt-1 break-all">POST {API_URL}</p>
              <p className="mt-2">Start your backend FastAPI server before using this page.</p>
            </div>
          </form>

          <div className="rounded-3xl border border-white/10 bg-white/8 p-6 shadow-2xl backdrop-blur-xl sm:p-8">
            <div className="mb-6 flex items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-white">Preview & Results</h2>
                <p className="mt-1 text-sm text-slate-300">Predictions are normalized to the 0 to 1 range.</p>
              </div>
              <div className="rounded-full bg-white/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">
                BehaviorAnalysis
              </div>
            </div>

            <div className="mb-6 overflow-hidden rounded-2xl border border-white/10 bg-black/30">
              {previewUrl ? (
                <video src={previewUrl} controls className="h-80 w-full object-cover" />
              ) : (
                <div className="flex h-80 items-center justify-center px-6 text-center text-slate-400">
                  Upload a video to preview and run inference.
                </div>
              )}
            </div>

            {result ? (
              <div className="space-y-4">
                <div className="mb-1 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">Big Five</div>
                {TRAIT_LABELS.map(([key, label]) => {
                  const value = Number(result?.traits?.[key] ?? 0);
                  return (
                    <div key={key} className="rounded-2xl bg-white/6 p-4">
                      <div className="mb-2 flex items-center justify-between text-sm">
                        <span className="font-semibold text-white">{label}</span>
                        <span className="text-slate-300">{value.toFixed(2)}</span>
                      </div>
                      <div className="h-2 rounded-full bg-white/10">
                        <div
                          className="h-2 rounded-full bg-linear-to-r from-cyan-400 to-fuchsia-400"
                          style={{ width: `${Math.max(0, Math.min(1, value)) * 100}%` }}
                        />
                      </div>
                    </div>
                  );
                })}

                {Object.keys(result?.direct_traits || {}).length > 0 && (
                  <div className="pt-3">
                    <div className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-fuchsia-200">
                      Direct Traits (Model Trained)
                    </div>
                    <div className="space-y-3">
                      {Object.entries(result.direct_traits).map(([key, raw]) => {
                        const value = Number(raw ?? 0);
                        return (
                          <div key={key} className="rounded-2xl bg-white/6 p-4">
                            <div className="mb-2 flex items-center justify-between text-sm">
                              <span className="font-semibold text-white">{toTitle(key)}</span>
                              <span className="text-slate-300">{value.toFixed(2)}</span>
                            </div>
                            <div className="h-2 rounded-full bg-white/10">
                              <div
                                className="h-2 rounded-full bg-linear-to-r from-fuchsia-400 to-cyan-400"
                                style={{ width: `${Math.max(0, Math.min(1, value)) * 100}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {Object.keys(result?.derived_scores || {}).length > 0 && (
                  <div className="pt-3">
                    <div className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-amber-200">
                      Derived Scores (Heuristic)
                    </div>
                    <div className="grid gap-2 sm:grid-cols-2">
                      {Object.entries(result.derived_scores).map(([key, raw]) => {
                        const value = Number(raw ?? 0);
                        const level = result?.score_levels?.[key];
                        return (
                          <div key={key} className="rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-sm">
                            <div className="font-medium text-white">{toTitle(key)}</div>
                            <div className="mt-1 text-slate-300">
                              {value.toFixed(2)}
                              {level ? ` (${level})` : ""}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {result?.behavior_analysis && (
                  <div className="pt-3">
                    <div className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-emerald-200">
                      Person, Expression & Voice Analysis
                    </div>
                    <div className="grid gap-3 sm:grid-cols-2">
                      {(() => {
                        const frame = result.behavior_analysis.frame_analysis || {};
                        const audio = result.behavior_analysis.audio_analysis || {};
                        const items = [
                          ["Person detected", frame.person_detected ? "Yes" : "No"],
                          ["Presence quality", frame.presence_quality || "N/A"],
                          ["Face detection rate", typeof frame.face_detection_rate !== "undefined" ? `${Math.round(frame.face_detection_rate * 100)}%` : "N/A"],
                          ["Frames with face", frame.frames_with_face ?? "N/A"],
                          ["Expression smile rate", typeof frame.expression_smile_rate !== "undefined" ? `${Math.round(frame.expression_smile_rate * 100)}%` : "N/A"],
                          ["Expression pattern", frame.expression_pattern || "N/A"],
                          ["Head motion score", frame.head_motion_score ?? "N/A"],
                          ["Posture stability", frame.posture_stability_score ?? "N/A"],
                          ["Visual engagement", frame.visual_engagement_score ?? "N/A"],
                          ["Reliability score", result.behavior_analysis.reliability_score ?? "N/A"],
                          ["Voice available", audio.voice_available ? "Yes" : "No"],
                          ["Talking pattern", audio.talking_pattern || audio.reason || "N/A"],
                          ["Speech rhythm", audio.speech_rhythm_score ?? "N/A"],
                          ["Pause ratio", audio.pause_ratio ?? "N/A"],
                        ];
                        return items.map(([label, value]) => (
                          <div key={label} className="rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-sm">
                            <div className="font-medium text-white">{label}</div>
                            <div className="mt-1 text-slate-300">{value}</div>
                          </div>
                        ));
                      })()}
                    </div>
                    {result.behavior_analysis.behavior_summary && (
                      <p className="mt-3 rounded-xl border border-emerald-400/20 bg-emerald-400/10 px-4 py-3 text-sm leading-6 text-slate-200">
                        {result.behavior_analysis.behavior_summary}
                      </p>
                    )}
                  </div>
                )}

                {result?.meta && Object.keys(result.meta).length > 0 && (
                  <div className="rounded-2xl border border-white/10 bg-black/20 p-4 text-xs leading-5 text-slate-300">
                    <p className="font-semibold text-white">Inference meta</p>
                    {result.meta.source_type && <p>Source: {result.meta.source_type}</p>}
                    {typeof result.meta.frames_used !== "undefined" && <p>Frames used: {result.meta.frames_used}</p>}
                  </div>
                )}

                <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 p-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <p className="text-sm font-semibold text-white">Career recommendation based on your personality</p>
                      <p className="mt-1 text-sm text-slate-300">Open the Career Path test page to combine these results with a short assessment.</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        try {
                          localStorage.setItem("behavior_analysis_result", JSON.stringify(result));
                        } catch (e) {}
                        navigate("/form");
                      }}
                      className="inline-flex items-center justify-center rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:scale-[1.01]"
                    >
                      Start career path test
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="rounded-2xl border border-white/10 bg-black/20 p-5 text-sm text-slate-300">
                Results will appear here after inference finishes.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BehaviorAnalysis;
