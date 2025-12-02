import React from "react";

const ResultPage = ({ result }) => {
  // Debug: Log the result to see what data we're receiving
  console.log("Result data:", result);

  // Parse the result based on PredictionOutput model
  const careerName =
    result?.["Best-Fit Career Domain"] ||
    result?.best_fit_career_domain ||
    "Career Recommendation";
  const careerRationale =
    result?.["Career Rationale"] ||
    result?.career_rationale ||
    "This career path aligns perfectly with your skills and interests.";
  const growthRoadmap =
    result?.["5-Year Career Growth Roadmap"] || result?.growth_roadmap || "";
  const skillGap =
    result?.["Skill Gap Analysis"] || result?.skill_gap_analysis || "";
  const recommendedCourses =
    result?.["Recommended Tools, Courses, and Certifications"] ||
    result?.recommended_courses ||
    "";
  const backupCareer =
    result?.["Alternative/Backup Career Option"] ||
    result?.backup_career_option ||
    "";
  const behavioralInsight =
    result?.["Behavioral Insight"] || result?.behavioral_insight || "";
  const confidenceScore =
    result?.["Confidence Score"] || result?.confidence_score || 0;

  // Parse skill gap into array
  const skillsArray = skillGap
    ? skillGap.split(/[,;.\n]/).filter((s) => s.trim()).slice(0, 6)
    : ["Problem Solving", "Communication", "Technical Knowledge", "Creativity"];

  // Parse growth roadmap into steps
  const roadmapSteps = growthRoadmap
    ? growthRoadmap.split(/[.\n]/).filter((s) => s.trim()).slice(0, 4)
    : ["Foundation Courses", "Intermediate Skills", "Advanced Projects", "Real-world Experience"];

  // Parse recommended courses
  const coursesArray = recommendedCourses
    ? recommendedCourses.split(/[,;.\n]/).filter((s) => s.trim()).slice(0, 3)
    : [];

  return (
    <div className="relative min-h-screen bg-linear-to-br from-blue-50 via-purple-50 to-pink-50 text-gray-900 font-poppins px-6 py-16 overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-400/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Header */}
      <div className="relative z-10 text-center mb-12 animate-fadeIn">
        <h1 className="text-5xl sm:text-6xl font-extrabold bg-linear-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
          Your AI Career Recommendation
        </h1>
        <p className="text-gray-600 text-lg">
          Discover your personalized career path powered by AI
        </p>
      </div>

      {/* Result Section */}
      <div className="relative z-10 max-w-7xl mx-auto animate-slideUp">
        {result ? (
          <div className="space-y-8">
            {/* Career Overview - Hero Box */}
            <div className="bg-linear-to-r from-blue-600 to-purple-600 rounded-3xl p-8 shadow-2xl text-white transform hover:scale-[1.02] transition-all duration-300">
              <div className="flex items-center gap-4 mb-4">
                <span className="text-5xl">🎯</span>
                <div className="flex-1">
                  <h2 className="text-3xl font-bold">{careerName}</h2>
                  <p className="text-blue-100 text-lg">
                    Your perfect career match
                  </p>
                  {confidenceScore > 0 && (
                    <div className="mt-2 flex items-center gap-2">
                      <span className="text-sm text-blue-200">
                        Confidence Score:
                      </span>
                      <div className="flex-1 max-w-xs bg-white/30 rounded-full h-2">
                        <div
                          className="bg-white h-2 rounded-full"
                          style={{ width: `${confidenceScore * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-bold text-white">
                        {(confidenceScore * 100).toFixed(0)}%
                      </span>
                    </div>
                  )}
                </div>
              </div>
              <p className="text-white/90 text-lg leading-relaxed">
                {careerRationale}
              </p>
            </div>

            {/* Grid Layout for Multiple Boxes */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Skill Gap Analysis Box */}
              <div className="bg-white rounded-3xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center gap-3 mb-6">
                  <span className="text-4xl">💡</span>
                  <h3 className="text-2xl font-bold text-gray-800">
                    Skills to Develop
                  </h3>
                </div>
                <div className="space-y-3">
                  {skillsArray.map((skill, i) => (
                    <div
                      key={i}
                      className="flex items-center gap-3 bg-linear-to-r from-blue-50 to-purple-50 p-3 rounded-xl"
                    >
                      <span className="text-blue-600 font-bold text-lg">✓</span>
                      <span className="text-gray-700 font-medium">
                        {skill.trim()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Career Growth Roadmap Box */}
              <div className="bg-white rounded-3xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center gap-3 mb-6">
                  <span className="text-4xl">📚</span>
                  <h3 className="text-2xl font-bold text-gray-800">
                    5-Year Growth Roadmap
                  </h3>
                </div>
                <div className="space-y-4">
                  {roadmapSteps.map((step, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <span className="bg-linear-to-r from-purple-500 to-pink-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm shrink-0">
                        {i + 1}
                      </span>
                      <p className="text-gray-700 font-medium pt-1">
                        {step.trim()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommended Courses & Certifications Box */}
              <div className="bg-linear-to-br from-green-50 to-emerald-50 rounded-3xl p-8 shadow-xl border border-green-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center gap-3 mb-6">
                  <span className="text-4xl">🎓</span>
                  <h3 className="text-2xl font-bold text-gray-800">
                    Recommended Learning
                  </h3>
                </div>
                <div className="space-y-3">
                  {coursesArray.length > 0 ? (
                    coursesArray.map((course, i) => (
                      <div key={i} className="bg-white p-4 rounded-xl">
                        <p className="text-gray-700 font-medium">
                          {course.trim()}
                        </p>
                      </div>
                    ))
                  ) : (
                    <div className="bg-white p-4 rounded-xl">
                      <p className="text-gray-700">{recommendedCourses}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Behavioral Insight & Backup Career Box */}
              <div className="bg-linear-to-br from-orange-50 to-red-50 rounded-3xl p-8 shadow-xl border border-orange-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center gap-3 mb-6">
                  <span className="text-4xl">🧠</span>
                  <h3 className="text-2xl font-bold text-gray-800">
                    Insights & Alternatives
                  </h3>
                </div>
                <div className="space-y-4">
                  <div className="bg-white p-4 rounded-xl">
                    <p className="text-gray-600 text-sm mb-2">
                      💭 Behavioral Insight
                    </p>
                    <p className="text-gray-700 font-medium">
                      {behavioralInsight}
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-xl">
                    <p className="text-gray-600 text-sm mb-2">
                      🔄 Alternative Career
                    </p>
                    <p className="text-orange-600 font-bold text-lg">
                      {backupCareer}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Resources & Next Steps Box */}
            <div className="bg-linear-to-r from-indigo-600 to-blue-600 rounded-3xl p-8 shadow-2xl text-white">
              <div className="flex items-center gap-3 mb-6">
                <span className="text-4xl">🚀</span>
                <h3 className="text-2xl font-bold">Resources & Next Steps</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-5 hover:bg-white/30 transition-all cursor-pointer">
                  <p className="font-semibold mb-2">📖 Online Courses</p>
                  <p className="text-sm text-blue-100">Coursera, Udemy, edX</p>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-5 hover:bg-white/30 transition-all cursor-pointer">
                  <p className="font-semibold mb-2">🎓 Certifications</p>
                  <p className="text-sm text-blue-100">Industry-recognized programs</p>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-5 hover:bg-white/30 transition-all cursor-pointer">
                  <p className="font-semibold mb-2">👥 Networking</p>
                  <p className="text-sm text-blue-100">LinkedIn, Meetups, Forums</p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap gap-4 justify-center pt-4">
              <button
                onClick={() => window.print()}
                className="bg-linear-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-4 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                📄 Download Report
              </button>
              <button
                onClick={() => (window.location.hash = "#/form")}
                className="bg-white hover:bg-gray-50 text-gray-800 font-semibold py-4 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 shadow-lg border-2 border-gray-200"
              >
                🔄 Try Another Assessment
              </button>
            </div>
          </div>
        ) : (
          <div className="text-center bg-white rounded-3xl p-12 shadow-2xl max-w-xl mx-auto">
            <span className="text-6xl mb-6 block">😕</span>
            <p className="text-2xl mb-6 text-gray-700 font-semibold">
              No result found
            </p>
            <p className="text-gray-600 mb-8">
              Please go back and submit the form to get your personalized career
              recommendation.
            </p>
            <button
              onClick={() => (window.location.hash = "#/form")}
              className="bg-linear-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-4 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              🔙 Go to Career Form
            </button>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="relative z-10 text-center mt-16 text-gray-500 text-sm">
        Powered by{" "}
        <span className="text-transparent bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text font-semibold">
          AI CareerPath
        </span>
      </div>
    </div>
  );
};

export default ResultPage;
