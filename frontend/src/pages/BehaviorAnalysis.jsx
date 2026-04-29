import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { postWithFallback } from "../api/client";

const TRAIT_LABELS = [
  ["openness", "Openness"],
  ["conscientiousness", "Conscientiousness"],
  ["extraversion", "Extraversion"],
  ["agreeableness", "Agreeableness"],
  ["neuroticism", "Neuroticism"],
];

const API_URL = import.meta.env.VITE_PERSONALITY_API_URL || "http://127.0.0.1:8000/personality/predict";
const CAREER_API_PATH = "/personality/recommend-career";

const CAREER_QUESTION_GROUPS = [
  {
    title: "Section 1 — Task Preference",
    questions: [
      {
        id: "q1",
        label: "Which activity do you enjoy the most?",
        options: [
          "Fixing technical problems or debugging systems",
          "Designing visuals or creative content",
          "Writing ideas, stories, or explanations",
          "Organizing, planning, or managing tasks",
        ],
      },
    ],
  },
  {
    title: "Section 2 — Problem-Solving Style",
    questions: [
      {
        id: "q2",
        label: "When you face a difficult problem, what is your natural approach?",
        options: [
          "Break it into logical steps and solve systematically",
          "Look for patterns or trends",
          "Discuss with others and get ideas",
          "Try different things until something works",
        ],
      },
    ],
  },
  {
    title: "Section 3 — Content Consumption",
    questions: [
      {
        id: "q3",
        label: "What type of content do you mostly explore online?",
        options: [
          "Technology, coding, gadgets",
          "Business, finance, startups",
          "Psychology, people, communication",
          "Art, design, entertainment",
        ],
      },
    ],
  },
  {
    title: "Section 4 — Group Role",
    questions: [
      {
        id: "q4",
        label: "In a group project, what role do you usually take?",
        options: [
          "Leader or decision-maker",
          "Technical/problem-solving contributor",
          "Creative/design/presentation role",
          "Supporter or coordinator",
        ],
      },
    ],
  },
  {
    title: "Section 5 — Learning Preference",
    questions: [
      {
        id: "q5",
        label: "Which type of topic is easiest for you to understand?",
        options: [
          "Numbers, formulas, calculations",
          "Concepts and theories",
          "Real-life case studies",
          "Visuals, diagrams, designs",
        ],
      },
    ],
  },
  {
    title: "Section 6 — Free Time Behavior",
    questions: [
      {
        id: "q6",
        label: "If you have a completely free day, what would you most likely do?",
        options: [
          "Build or code something",
          "Watch business or money-related content",
          "Create content (videos/designs/writing)",
          "Learn about people or psychology",
        ],
      },
    ],
  },
  {
    title: "Section 7 — Career Attraction",
    questions: [
      {
        id: "q7",
        label: "Which of these sounds most interesting to you?",
        options: [
          "Building apps or software",
          "Running a business or managing money",
          "Creating media or designs",
          "Helping people solve problems",
        ],
      },
    ],
  },
  {
    title: "Section 8 — Work Style",
    questions: [
      {
        id: "q8",
        label: "What kind of work environment do you prefer?",
        options: [
          "Independent and focused",
          "Team-based and interactive",
          "Flexible and creative",
          "Structured and organized",
        ],
      },
    ],
  },
  {
    title: "Section 9 — Decision Style",
    questions: [
      {
        id: "q9",
        label: "How do you usually make decisions?",
        options: [
          "Based on logic and data",
          "Based on creativity or intuition",
          "Based on advice from others",
          "Based on past experience",
        ],
      },
    ],
  },
  {
    title: "Section 10 — Motivation",
    questions: [
      {
        id: "q10",
        label: "What motivates you the most?",
        options: [
          "Solving complex problems",
          "Earning money and success",
          "Expressing creativity",
          "Helping others",
        ],
      },
    ],
  },
  {
    title: "Section 11 — Favorite Subject",
    questions: [
      {
        id: "q11",
        label: "Which subject do you like the most?",
        options: [
          "Mathematics",
          "Computer Science / IT",
          "Business / Economics",
          "Biology / Health Sciences",
          "Arts / Design",
          "Social Studies / Psychology",
        ],
      },
    ],
  },
  {
    title: "Section 12 — Strongest Subject",
    questions: [
      {
        id: "q12",
        label: "In which subject do you perform the best?",
        options: [
          "Mathematics",
          "Computer Science / IT",
          "Business / Economics",
          "Biology / Health Sciences",
          "Arts / Design",
          "Social Studies / Psychology",
        ],
      },
    ],
  },
  {
    title: "Section 13 — Scenario: School Project",
    questions: [
      {
        id: "q13",
        label: "You are assigned a project. What part do you choose?",
        options: [
          "Coding or technical implementation",
          "Designing slides or visuals",
          "Researching and writing content",
          "Managing team and deadlines",
        ],
      },
    ],
  },
  {
    title: "Section 14 — Scenario: Startup Idea",
    questions: [
      {
        id: "q14",
        label: "If you start a small project/startup, what would you focus on?",
        options: [
          "Building the product (technical side)",
          "Marketing and selling it",
          "Designing the user experience",
          "Managing operations and planning",
        ],
      },
    ],
  },
  {
    title: "Section 15 — Scenario: Problem Situation",
    questions: [
      {
        id: "q15",
        label: "A system/app is not working. What do you do first?",
        options: [
          "Debug and find the root cause",
          "Look for similar solutions online",
          "Ask someone experienced",
          "Try quick fixes",
        ],
      },
    ],
  },
  {
    title: "Section 16 — Scenario: Event Management",
    questions: [
      {
        id: "q16",
        label: "You are organizing an event. What role do you take?",
        options: [
          "Planning and coordination",
          "Promotion and communication",
          "Designing posters/content",
          "Handling technical setup",
        ],
      },
    ],
  },
  {
    title: "Section 17 — Scenario: Learning Something New",
    questions: [
      {
        id: "q17",
        label: "How do you prefer to learn a new skill?",
        options: [
          "Practice and hands-on work",
          "Watching tutorials",
          "Reading and understanding theory",
          "Learning with others",
        ],
      },
    ],
  },
  {
    title: "Section 18 — Scenario: Career Choice Thought",
    questions: [
      {
        id: "q18",
        label: "Which situation sounds more exciting to you?",
        options: [
          "Solving a complex technical problem",
          "Closing a big business deal",
          "Creating something visually appealing",
          "Helping someone improve their life",
        ],
      },
    ],
  },
];

const QUESTION_COUNT = 18;

const toTitle = (key) =>
  String(key)
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

const buildInitialCareerForm = () => {
  const entries = {};
  CAREER_QUESTION_GROUPS.forEach((group) => {
    group.questions.forEach((question) => {
      entries[question.id] = "";
    });
  });
  entries.additional_notes = "";
  return entries;
};

const BehaviorAnalysis = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [showCareerForm, setShowCareerForm] = useState(false);
  const [careerForm, setCareerForm] = useState(buildInitialCareerForm);
  const [careerLoading, setCareerLoading] = useState(false);
  const [careerError, setCareerError] = useState("");
  const [careerResult, setCareerResult] = useState(null);

  const isVideo = useMemo(() => {
    if (!file) {
      return false;
    }
    return file.type.startsWith("video/");
  }, [file]);

  const requiredAnswers = useMemo(
    () =>
      CAREER_QUESTION_GROUPS.flatMap((group) => group.questions).filter((question) =>
        String(careerForm[question.id] || "").trim().length > 0,
      ).length,
    [careerForm],
  );

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
    setShowCareerForm(false);
    setCareerForm(buildInitialCareerForm());
    setCareerResult(null);
    setCareerError("");

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
      setError("Select an image or video first.");
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
    } catch (predictionError) {
      setError(predictionError.message || "Unable to analyze the file.");
    } finally {
      setLoading(false);
    }
  };

  const handleCareerFieldChange = (fieldId, value) => {
    setCareerForm((current) => ({
      ...current,
      [fieldId]: value,
    }));
  };

  const handleCareerSubmit = async (event) => {
    event.preventDefault();

    if (!result) {
      setCareerError("Run personality analysis first.");
      return;
    }

    const requiredValues = CAREER_QUESTION_GROUPS.flatMap((group) => group.questions.map((question) => careerForm[question.id]));
    if (requiredValues.some((value) => !String(value || "").trim())) {
      setCareerError("Please answer all 18 career questions before submitting.");
      return;
    }

    setCareerLoading(true);
    setCareerError("");
    setCareerResult(null);

    try {
      const payload = {
        personality_score: result,
        questionnaire_responses: CAREER_QUESTION_GROUPS.reduce((accumulator, group) => {
          group.questions.forEach((question) => {
            accumulator[question.label] = careerForm[question.id];
          });
          return accumulator;
        }, {}),
        additional_notes: careerForm.additional_notes,
      };

      const data = await postWithFallback(CAREER_API_PATH, payload, { timeoutMs: 60000 });
      const recommendation = data?.recommendation || null;
      setCareerResult(recommendation);

      const resultPayload = {
        recommendation,
        personality_score: result,
        questionnaire_responses: payload.questionnaire_responses,
        additional_notes: payload.additional_notes,
        generated_at: new Date().toISOString(),
      };

      localStorage.setItem("behavior_career_result", JSON.stringify(resultPayload));
      navigate("/behavior-career-result", { state: resultPayload });
    } catch (recommendationError) {
      setCareerError(recommendationError.message || "Unable to generate career recommendation.");
    } finally {
      setCareerLoading(false);
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
            Upload an image or video and get rich personality insights.
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
                  accept="image/*,video/*"
                  onChange={handleFileChange}
                  className="hidden"
                />
                <div className="space-y-2">
                  <div className="text-lg font-semibold text-white">Choose a face image or a short video</div>
                  <div className="text-sm text-slate-300">JPG, PNG, MP4, MOV, WEBM</div>
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
                isVideo ? (
                  <video src={previewUrl} controls className="h-80 w-full object-cover" />
                ) : (
                  <img src={previewUrl} alt="Selected preview" className="h-80 w-full object-cover" />
                )
              ) : (
                <div className="flex h-80 items-center justify-center px-6 text-center text-slate-400">
                  Upload a photo or video to preview the subject and run inference.
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
                      <p className="mt-1 text-sm text-slate-300">
                        Answer the assessment and combine it with your personality score for a more targeted career path.
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={() => setShowCareerForm((current) => !current)}
                      className="inline-flex items-center justify-center rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:scale-[1.01]"
                    >
                      {showCareerForm ? "Hide questionnaire" : "Open questionnaire"}
                    </button>
                  </div>
                </div>

                {showCareerForm && (
                  <form onSubmit={handleCareerSubmit} className="space-y-5 rounded-3xl border border-white/10 bg-black/20 p-5 sm:p-6">
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">Questionnaire</p>
                      <h3 className="mt-2 text-xl font-bold text-white">Full Career Assessment Questionnaire</h3>
                      <p className="mt-1 text-sm text-slate-300">
                        Answer all 18 questions. Your personality score is sent alongside these responses.
                      </p>
                    </div>

                    <div className="space-y-5">
                      {CAREER_QUESTION_GROUPS.map((group) => (
                        <div key={group.title} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <h4 className="text-sm font-semibold uppercase tracking-[0.18em] text-fuchsia-200">{group.title}</h4>
                          <div className="mt-4 space-y-5">
                            {group.questions.map((question) => (
                              <fieldset key={question.id} className="space-y-3">
                                <legend className="text-sm font-semibold text-white">{question.label}</legend>
                                <div className="grid gap-3">
                                  {question.options.map((option) => (
                                    <label
                                      key={option}
                                      className={`cursor-pointer rounded-xl border px-4 py-3 text-sm transition ${
                                        careerForm[question.id] === option
                                          ? "border-cyan-400 bg-cyan-400/15 text-white"
                                          : "border-white/10 bg-black/20 text-slate-200 hover:border-white/20"
                                      }`}
                                    >
                                      <input
                                        type="radio"
                                        name={question.id}
                                        value={option}
                                        checked={careerForm[question.id] === option}
                                        onChange={() => handleCareerFieldChange(question.id, option)}
                                        className="sr-only"
                                      />
                                      {option}
                                    </label>
                                  ))}
                                </div>
                              </fieldset>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                      <label className="block text-sm font-semibold text-white">
                        Additional notes
                        <span className="ml-2 text-xs font-normal text-slate-400">Optional text-based input</span>
                      </label>
                      <textarea
                        value={careerForm.additional_notes}
                        onChange={(event) => handleCareerFieldChange("additional_notes", event.target.value)}
                        rows={4}
                        placeholder="Anything else you'd like the career model to consider..."
                        className="mt-3 w-full rounded-2xl border border-white/10 bg-black/25 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400"
                      />
                    </div>

                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <p className="text-xs text-slate-400">
                        Completed {requiredAnswers} of {QUESTION_COUNT} required questions.
                      </p>
                      <button
                        type="submit"
                        disabled={careerLoading}
                        className="inline-flex items-center justify-center rounded-2xl bg-linear-to-r from-emerald-400 to-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        {careerLoading ? "Generating recommendation..." : "Get career recommendation"}
                      </button>
                    </div>

                    {careerError && (
                      <p className="rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
                        {careerError}
                      </p>
                    )}

                    {careerResult && (
                      <div className="space-y-4 rounded-2xl border border-emerald-400/20 bg-emerald-400/10 p-4">
                        <div>
                          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-200">Recommended career path</p>
                          <h4 className="mt-2 text-2xl font-black text-white">{careerResult.career_path || "Career recommendation"}</h4>
                        </div>

                        {careerResult.rationale && (
                          <div className="rounded-xl bg-black/20 p-4 text-sm leading-6 text-slate-200">
                            {careerResult.rationale}
                          </div>
                        )}

                        {Array.isArray(careerResult.best_fit_roles) && careerResult.best_fit_roles.length > 0 && (
                          <div>
                            <p className="text-sm font-semibold text-white">Best fit roles</p>
                            <div className="mt-2 flex flex-wrap gap-2">
                              {careerResult.best_fit_roles.map((role) => (
                                <span key={role} className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-100">
                                  {role}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {Array.isArray(careerResult.skills_to_build) && careerResult.skills_to_build.length > 0 && (
                          <div>
                            <p className="text-sm font-semibold text-white">Skills to build</p>
                            <ul className="mt-2 space-y-2 text-sm text-slate-200">
                              {careerResult.skills_to_build.map((skill) => (
                                <li key={skill} className="rounded-xl bg-black/20 px-3 py-2">
                                  {skill}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {Array.isArray(careerResult.roadmap) && careerResult.roadmap.length > 0 && (
                          <div>
                            <p className="text-sm font-semibold text-white">Roadmap</p>
                            <ol className="mt-2 space-y-2 text-sm text-slate-200">
                              {careerResult.roadmap.map((step, index) => (
                                <li key={`${step}-${index}`} className="rounded-xl bg-black/20 px-3 py-2">
                                  {step}
                                </li>
                              ))}
                            </ol>
                          </div>
                        )}

                        {typeof careerResult.confidence !== "undefined" && (
                          <p className="text-xs text-slate-300">
                            Confidence: {Number(careerResult.confidence).toFixed(2)}
                          </p>
                        )}
                      </div>
                    )}
                  </form>
                )}
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
