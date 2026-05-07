/*
Scholarship finder page. It collects student preferences and shows matching scholarship opportunities from the backend.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

import React, { useMemo, useState } from "react";
import { postWithFallback } from "../api/client";

const DEGREE_OPTIONS = ["BS", "MS", "PhD"];
const UNIVERSITY_TYPE_OPTIONS = ["Any", "Government", "Private"];
const FUNDING_OPTIONS = ["Fully funded", "Partially funded", "Any"];

const ScholarshipFinder = () => {
  const [form, setForm] = useState({
    degree_level: "MS",
    field_of_study: "Computer Science",
    country: "Germany",
    university_type: "Any",
    funding_type: "Fully funded",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const userId = useMemo(() => {
    const existing = localStorage.getItem("cp_user_id");
    if (existing) return existing;
    const generated = `cp_${Date.now()}`;
    localStorage.setItem("cp_user_id", generated);
    return generated;
  }, []);

  const updateField = (name, value) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const submitSearch = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const payload = {
        ...form,
        user_id: userId,
        max_results: 10,
      };
      const response = await postWithFallback("/chatbot/scholarships/search", payload, {
        timeoutMs: 120000,
      });

      setResult(response);
    } catch (err) {
      setError(err.message || "Failed to find scholarships");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-linear-to-br from-emerald-50 via-sky-50 to-indigo-50 overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-24 -left-10 w-96 h-96 bg-emerald-300/20 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-20 w-md h-112 bg-cyan-300/20 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center justify-between gap-3">
          <div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900">Find Scholarships</h1>
            <p className="text-gray-600 mt-2">
              Search the web with your preferences and get AI-structured scholarship recommendations.
            </p>
          </div>
          <button
            onClick={() => {
              window.location.hash = "#/dashboard";
            }}
            className="bg-white border border-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold hover:bg-gray-50"
          >
            Back to Dashboard
          </button>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
          <div className="xl:col-span-2 bg-white/85 backdrop-blur-md rounded-2xl border border-gray-200 shadow-lg p-6 h-max">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Scholarship Preferences</h2>

            <form onSubmit={submitSearch} className="space-y-4">
              <div>
                <label className="block text-sm text-gray-700 mb-1">Degree Level</label>
                <select
                  value={form.degree_level}
                  onChange={(e) => updateField("degree_level", e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 bg-white"
                >
                  {DEGREE_OPTIONS.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-700 mb-1">Field of Study</label>
                <input
                  type="text"
                  value={form.field_of_study}
                  onChange={(e) => updateField("field_of_study", e.target.value)}
                  placeholder="e.g. Computer Science, Mechanical Engineering"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm text-gray-700 mb-1">Scholarship Country</label>
                <input
                  type="text"
                  value={form.country}
                  onChange={(e) => updateField("country", e.target.value)}
                  placeholder="e.g. USA, Germany, Canada"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm text-gray-700 mb-1">University Type</label>
                <select
                  value={form.university_type}
                  onChange={(e) => updateField("university_type", e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 bg-white"
                >
                  {UNIVERSITY_TYPE_OPTIONS.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-700 mb-1">Funding Type</label>
                <select
                  value={form.funding_type}
                  onChange={(e) => updateField("funding_type", e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 bg-white"
                >
                  {FUNDING_OPTIONS.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-linear-to-r from-emerald-600 to-cyan-600 text-white py-2.5 rounded-lg font-semibold hover:from-emerald-700 hover:to-cyan-700 disabled:opacity-60"
              >
                {loading ? "Searching Scholarships..." : "Search Scholarships"}
              </button>
            </form>

            {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
          </div>

          <div className="xl:col-span-3 bg-white/80 backdrop-blur-md rounded-2xl border border-gray-200 shadow-lg p-6">
            {!result && !loading && (
              <div className="text-gray-600 text-sm">
                Submit your preferences to get scholarship options with:
                <ul className="mt-2 list-disc pl-5 space-y-1">
                  <li>University name</li>
                  <li>Scholarship name</li>
                  <li>Stipend and funding details</li>
                  <li>Requirements and required documents</li>
                  <li>Application links and source references</li>
                </ul>
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="mb-6 inline-block">
                  <div className="relative w-16 h-16">
                    <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-emerald-600 border-r-cyan-600 animate-spin"></div>
                    <div className="absolute inset-2 rounded-full border-4 border-transparent border-t-cyan-600 border-r-emerald-600 animate-spin" style={{ animationDirection: "reverse", animationDuration: "2s" }}></div>
                    <div className="absolute inset-4 rounded-full bg-linear-to-r from-emerald-500 to-cyan-500 flex items-center justify-center">
                      <div className="text-white text-lg animate-pulse">🔍</div>
                    </div>
                  </div>
                </div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  <span className="bg-linear-to-r from-emerald-600 to-cyan-600 bg-clip-text text-transparent">
                    Searching Scholarships
                  </span>
                </h3>
                <p className="text-gray-600 text-sm">
                  Searching live web sources and preparing an AI response...
                </p>
                <div className="flex gap-1 mt-4">
                  <div className="w-2 h-2 bg-emerald-600 rounded-full animate-bounce" style={{ animationDelay: "0s" }}></div>
                  <div className="w-2 h-2 bg-cyan-600 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                  <div className="w-2 h-2 bg-emerald-600 rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
                </div>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-lg font-bold text-gray-800">Search Summary</h2>
                  <p className="text-gray-700 mt-2">{result.summary || "No summary available."}</p>
                  {result.search_query && (
                    <p className="text-xs text-gray-500 mt-2">Query: {result.search_query}</p>
                  )}
                  <p className="text-xs text-gray-500 mt-1">
                    Results found: {Array.isArray(result.scholarships) ? result.scholarships.length : 0}
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-gray-800 mb-3">Scholarship List</h3>
                  {(result.scholarships || []).length === 0 ? (
                    <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
                      No scholarship entries were returned for this query. Try changing country, degree, or funding type.
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {(result.scholarships || []).map((item, index) => (
                      <div key={`${item.scholarship_name}-${index}`} className="border border-gray-200 rounded-xl p-4 bg-white/90">
                        <div className="flex flex-wrap items-center gap-2 justify-between">
                          <h4 className="text-base font-bold text-gray-900">{item.scholarship_name || "Scholarship"}</h4>
                          <span className="text-xs px-2 py-1 rounded-full bg-emerald-100 text-emerald-700">
                            {item.funding_type || "Funding not specified"}
                          </span>
                        </div>

                        <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-700">
                          <p><span className="font-semibold">University:</span> {item.university_name || "Not clearly specified"}</p>
                          <p><span className="font-semibold">Country:</span> {item.country || "Not clearly specified"}</p>
                          <p><span className="font-semibold">Degree:</span> {item.degree_level || "Not clearly specified"}</p>
                          <p><span className="font-semibold">Field:</span> {item.field_of_study || "Not clearly specified"}</p>
                          <p><span className="font-semibold">Stipend:</span> {item.stipend || "Not clearly specified"}</p>
                          <p><span className="font-semibold">Tuition Coverage:</span> {item.tuition_coverage || "Not clearly specified"}</p>
                          <p><span className="font-semibold">Deadline:</span> {item.deadline || "Not clearly specified"}</p>
                          <p><span className="font-semibold">University Type:</span> {item.university_type || "Not clearly specified"}</p>
                        </div>

                        <div className="mt-3 text-sm text-gray-700">
                          <p className="font-semibold">Requirements:</p>
                          <ul className="list-disc pl-5 mt-1 space-y-1">
                            {(item.requirements || []).map((req, reqIndex) => (
                              <li key={`${req}-${reqIndex}`}>{req}</li>
                            ))}
                          </ul>
                        </div>

                        <div className="mt-3 text-sm text-gray-700">
                          <p className="font-semibold">Documents Needed:</p>
                          <ul className="list-disc pl-5 mt-1 space-y-1">
                            {(item.documents_needed || []).map((doc, docIndex) => (
                              <li key={`${doc}-${docIndex}`}>{doc}</li>
                            ))}
                          </ul>
                        </div>

                        <p className="mt-3 text-sm text-gray-700">
                          <span className="font-semibold">Application Process:</span> {item.application_process || "Not clearly specified"}
                        </p>

                        <div className="mt-3 flex flex-wrap gap-3 text-sm">
                          {item.application_link && (
                            <a
                              href={item.application_link}
                              target="_blank"
                              rel="noreferrer"
                              className="text-cyan-700 font-semibold hover:underline"
                            >
                              Application Link
                            </a>
                          )}
                          {item.source_link && (
                            <a
                              href={item.source_link}
                              target="_blank"
                              rel="noreferrer"
                              className="text-emerald-700 font-semibold hover:underline"
                            >
                              Source
                            </a>
                          )}
                        </div>

                        {item.notes && <p className="mt-3 text-sm text-gray-600">{item.notes}</p>}
                      </div>
                      ))}
                    </div>
                  )}
                </div>

                {(result.checklist || []).length > 0 && (
                  <div>
                    <h3 className="text-lg font-bold text-gray-800 mb-2">Scholarship Application Checklist</h3>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-700">
                      {result.checklist.map((item, index) => (
                        <li key={`${item}-${index}`}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScholarshipFinder;