import React, { useState, useMemo, useEffect } from "react";
import Loader from "../assets/components/Loader";
import ResumeUploadForm from "../assets/components/ResumeUploadForm";

// Education mapping for dynamic skills/certs
const EDUCATION_MAP = {
  "BS Software Engineering": {
    skills: [
      "JavaScript",
      "React",
      "Node.js",
      "REST",
      "Databases",
      "Version Control",
      "APIs",
      "Data Structures",
      "Algorithms",
      "Docker",
      "Git",
    ],
    certs: [
      "Full-Stack Web Dev Certificate",
      "Oracle Java Certificate",
      "AWS Developer Associate",
      "Google Front-End",
    ],
  },
  "BSc Computer Science": {
    skills: [
      "Python",
      "SQL",
      "ETL",
      "Spark",
      "Cloud",
      "Model Deployment",
      "Kubernetes",
      "MLOps",
      "Data Warehousing",
      "Docker",
      "Git",
    ],
    certs: [
      "Google Cloud Data Engineer",
      "AWS Big Data",
      "Google Professional ML Engineer",
      "AWS ML Specialty",
    ],
  },
  "BSc Data Science": {
    skills: [
      "Python",
      "Pandas",
      "Machine Learning",
      "Statistics",
      "Data Visualization",
      "SQL",
      "Spark",
      "ETL",
      "Data Warehousing",
      "Cloud",
      "Model Deployment",
    ],
    certs: [
      "IBM Data Science Certificate",
      "TensorFlow Developer Certificate",
      "AWS ML Specialty",
      "Google Professional ML Engineer",
    ],
  },
  "MS Data Science": {
    skills: [
      "Python",
      "Spark",
      "ETL",
      "Cloud",
      "MLOps",
      "Model Deployment",
      "Data Warehousing",
      "Kubernetes",
      "Docker",
      "SQL",
      "Statistics",
    ],
    certs: [
      "AWS Big Data",
      "Google Cloud Data Engineer",
      "AWS ML Specialty",
      "TensorFlow Developer Certificate",
    ],
  },
  "MSc Computer Science": {
    skills: [
      "Python",
      "Cloud",
      "Kubernetes",
      "Docker",
      "Model Deployment",
      "Data Structures",
      "Algorithms",
      "Version Control",
      "React",
      "APIs",
    ],
    certs: [
      "Google Front-End",
      "Oracle Java Certificate",
      "AWS Developer Associate",
      "Google Professional ML Engineer",
    ],
  },
  "MBA": {
    skills: [
      "Market Research",
      "Stakeholder Mgmt",
      "Prioritization",
      "Roadmapping",
      "Data-driven Decisions",
      "Excel",
      "Project Management",
      "Communication",
    ],
    certs: ["CSPO", "Pragmatic Institute", "FMVA", "AgileBA"],
  },
  "BBA Finance": {
    skills: [
      "Financial Modeling",
      "Accounting",
      "Forecasting",
      "Excel",
      "SQL",
      "Reporting",
      "Stakeholder Mgmt",
      "Business Analysis",
    ],
    certs: ["CFA Level 1", "FMVA", "AgileBA", "Excel"],
  },
  "BS Statistics": {
    skills: [
      "Statistics",
      "Python",
      "R",
      "SQL",
      "Data Visualization",
      "Forecasting",
      "Reporting",
      "Excel",
      "Pandas",
    ],
    certs: [
      "IBM Data Science Certificate",
      "CFA Level 1",
      "TensorFlow Developer Certificate",
    ],
  },
  "BS Biotechnology": {
    skills: [
      "Python",
      "R",
      "Genomics",
      "Sequence Analysis",
      "Statistics",
      "Data Cleaning",
      "Clinical Data Management",
      "Regulatory",
      "SAS",
      "GCP",
    ],
    certs: ["Bioinformatics Cert", "CDM Cert", "GCP", "AWS ML Specialty"],
  },
  "BSc Nursing": {
    skills: [
      "Clinical Knowledge",
      "Patient Care",
      "Medication Admin",
      "Communication",
      "Monitoring Tools",
      "EMR Systems",
    ],
    certs: ["RN License", "BLS", "PHR", "Teaching License"],
  },
  "MBBS": {
    skills: [
      "Clinical Knowledge",
      "Patient Care",
      "Medication Admin",
      "Regulatory",
      "GCP",
      "Data Cleaning",
      "Communication",
    ],
    certs: ["RN License", "BLS", "GCP", "CDM Cert"],
  },
  "BDS": {
    skills: [
      "Clinical Knowledge",
      "Patient Care",
      "Communication",
      "Regulatory",
      "SAS",
      "GCP",
    ],
    certs: ["RN License", "GCP", "CDM Cert", "BLS"],
  },
  "BS Mechanical Engineering": {
    skills: [
      "AutoCAD",
      "Structural Analysis",
      "Surveying",
      "Project Mgmt",
      "MS Project",
      "Revit",
      "SAP2000",
    ],
    certs: ["Autodesk Revit", "PE Equivalent", "MS Project"],
  },
  "BS Civil Engineering": {
    skills: [
      "AutoCAD",
      "Surveying",
      "Structural Analysis",
      "Project Mgmt",
      "Stakeholder Mgmt",
      "Data-driven Decisions",
    ],
    certs: ["Autodesk Revit", "PE Equivalent", "MS Project"],
  },
  "B.Arch": {
    skills: [
      "AutoCAD",
      "Surveying",
      "Structural Analysis",
      "Project Mgmt",
      "Figma",
      "Wireframing",
      "UX Research",
    ],
    certs: ["Autodesk Revit", "NN/g UX Cert", "Google UX Design"],
  },
  "BA Psychology": {
    skills: [
      "Communication",
      "Stakeholder Mgmt",
      "Business Analysis",
      "Excel",
      "Lesson Planning",
      "Assessment",
      "User Research",
      "Data Visualization",
    ],
    certs: ["TESOL", "Teaching License", "AgileBA", "Google UX Design"],
  },
  "BA Fine Arts": {
    skills: [
      "Figma",
      "Wireframing",
      "UX Research",
      "Prototyping",
      "User Testing",
      "Creativity",
      "Typography",
      "Layout",
      "Illustrator",
      "Photoshop",
    ],
    certs: ["Adobe Cert", "Google UX Design", "NN/g UX Cert", "InDesign"],
  },
  "High School Diploma": {
    skills: [
      "Communication",
      "Excel",
      "Basic Python",
      "HTML",
      "CSS",
      "JavaScript",
      "Problem Solving",
    ],
    certs: ["Google Front-End", "TESOL", "Full-Stack Web Dev Certificate"],
  },
};

const GENERIC_CERTS = [
  "AWS ML Specialty",
  "Google Front-End",
  "Oracle Java Certificate",
  "Full-Stack Web Dev Certificate",
  "CFA Level 1",
  "FMVA",
  "AgileBA",
  "CSPO",
  "Pragmatic Institute",
  "TensorFlow Developer Certificate",
  "Google Professional ML Engineer",
  "Google Cloud Data Engineer",
  "Bioinformatics Cert",
  "CDM Cert",
  "GCP",
  "RN License",
  "BLS",
  "TESOL",
  "Teaching License",
  "Adobe Cert",
  "NN/g UX Cert",
];

// Grouped options derived from dataset themes
const GROUPS = {
  generic: {
    skills: [
      "Communication",
      "Excel",
      "Git",
      "Project Management",
      "SQL",
      "Python",
      "JavaScript",
      "Problem Solving",
    ],
    interests: [
      "Data",
      "AI",
      "Technology",
      "Business",
      "Research",
      "Design",
      "Education",
      "Healthcare",
    ],
  },
  cs_data: {
    skills: [
      "Python",
      "SQL",
      "Pandas",
      "Machine Learning",
      "Data Visualization",
      "ETL",
      "Spark",
      "Docker",
      "Kubernetes",
      "Model Deployment",
      "React",
      "Node.js",
      "REST",
      "Databases",
      "Cloud",
    ],
    interests: [
      "Data",
      "AI",
      "Backend",
      "Frontend",
      "Cloud",
      "Security",
      "DevOps",
      "Research",
      "Product",
    ],
  },
  bio_clinical: {
    skills: [
      "Genomics",
      "Sequence Analysis",
      "R",
      "Python",
      "Statistics",
      "Clinical Data Management",
      "GCP",
      "Regulatory",
      "SAS",
      "Data Cleaning",
    ],
    interests: ["Healthcare", "Biotech", "Genomics", "Research", "Data"],
  },
  civil_mech_arch: {
    skills: [
      "AutoCAD",
      "Structural Analysis",
      "Surveying",
      "Project Management",
      "MS Project",
      "Revit",
      "SAP2000",
    ],
    interests: [
      "Construction",
      "Design",
      "Sustainability",
      "Engineering",
    ],
  },
  finance_stats: {
    skills: [
      "Excel",
      "Financial Modeling",
      "Forecasting",
      "Accounting",
      "SQL",
      "Power BI",
      "Tableau",
    ],
    interests: ["Finance", "Business", "Economics", "Research", "Data"],
  },
  ux_product_design: {
    skills: [
      "UX Research",
      "Figma",
      "Wireframing",
      "Prototyping",
      "User Testing",
      "IA",
      "Photoshop",
      "Illustrator",
      "Market Research",
      "Stakeholder Mgmt",
      "Roadmapping",
      "Prioritization",
    ],
    interests: [
      "UX",
      "Design",
      "Product",
      "Marketing",
      "Social Impact",
      "Arts",
    ],
  },
  nursing: {
    skills: [
      "Patient Care",
      "Clinical Knowledge",
      "Medication Admin",
      "EMR Systems",
      "Monitoring Tools",
      "Communication",
    ],
    interests: [
      "Healthcare",
      "Social Impact",
      "Education",
    ],
  },
};

// Education Level -> group
const mapEducationToGroup = (edu = "") => {
  const e = edu.toLowerCase();
  if (/(software|computer)/.test(e)) return "cs_data";
  if (/(data science|ms data|statistics)/.test(e)) return "cs_data";
  if (/(biotechnology|bio|mbbs|bds|nursing)/.test(e))
    return e.includes("nursing") ? "nursing" : "bio_clinical";
  if (/(civil|mechanical|arch)/.test(e)) return "civil_mech_arch";
  if (/(bba finance|finance)/.test(e)) return "finance_stats";
  if (/(psychology|fine arts|mba)/.test(e)) return "ux_product_design";
  if (/(high school|diploma)/.test(e)) return "generic";
  return "generic";
};

// Multi-page form component
const MultiPageCareerForm = ({ onSubmit, loading }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    educationLevel: "",
    academicPerformance: "",
    workPreference: "",
    problemSolving: "",
    environmentPreference: "",
    teamworkPreference: "",
    learningStyle: "",
    skillsSelected: new Set(),
    skillsOther: "",
    certifications: "",
    interestsSelected: new Set(),
    interestsOther: "",
    extraCurricular: "",
  });

  const educationOptions = Object.keys(EDUCATION_MAP);
  const workPrefOptions = ["Data", "People", "Ideas"];
  const problemSolvingOptions = [
    "Analytical and logical",
    "Empathetic and structured",
    "Creative and iterative",
    "Strategic and analytical",
  ];
  const environmentOptions = ["Structured", "Flexible"];
  const teamworkOptions = ["Independently", "In a team", "Both"];
  const learningStyleOptions = ["Practice", "Observation", "Theory"];

  const interestsBase = {
    data: [
      "Data",
      "AI",
      "Cloud",
      "Security",
      "Backend",
      "Frontend",
      "DevOps",
      "Product",
      "Research",
      "Sustainability",
    ],
    people: [
      "Education",
      "Healthcare",
      "Social Impact",
      "HR",
      "Community",
      "Counseling",
      "Training",
    ],
    ideas: [
      "Design",
      "UX",
      "Marketing",
      "Entrepreneurship",
      "Arts",
      "Product",
      "Innovation",
    ],
  };

  const eduData =
    EDUCATION_MAP[formData.educationLevel] || { skills: [], certs: GENERIC_CERTS };
  const dynamicSkills = eduData.skills;
  const dynamicCerts = [...new Set([...eduData.certs, ...GENERIC_CERTS])];
  const dynamicInterests = formData.workPreference
    ? interestsBase[formData.workPreference.toLowerCase()]
    : [];

  const toggleSet = (setterKey, value) => {
    setFormData((prev) => {
      const set = new Set(prev[setterKey]);
      set.has(value) ? set.delete(value) : set.add(value);
      return { ...prev, [setterKey]: set };
    });
  };

  const handleInputChange = (key, value) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleNext = () => {
    if (validatePage(currentPage)) {
      setCurrentPage(currentPage + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleBack = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const validatePage = (page) => {
    if (page === 1) {
      return (
        formData.fullName.trim() &&
        formData.email.trim() &&
        formData.educationLevel
      );
    }
    if (page === 2) {
      return (
        formData.workPreference &&
        formData.problemSolving &&
        formData.environmentPreference &&
        formData.teamworkPreference &&
        formData.learningStyle
      );
    }
    if (page === 3) {
      return formData.skillsSelected.size > 0;
    }
    return true;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validatePage(4)) {
      alert("Please select at least one interest.");
      return;
    }

    const skillsCombined = [
      ...formData.skillsSelected,
      ...(formData.skillsOther
        ? formData.skillsOther.split(/[;,]/).map((x) => x.trim()).filter(Boolean)
        : []),
    ].join("; ");

    const interestsCombined = [
      ...formData.interestsSelected,
      ...(formData.interestsOther
        ? formData.interestsOther.split(/[;,]/).map((x) => x.trim()).filter(Boolean)
        : []),
    ].join("; ");

    const userId = localStorage.getItem("cp_user_id") || `user_${Date.now()}`;
    localStorage.setItem("cp_user_id", userId);

    const payload = {
      "User ID": userId,
      "Full Name": formData.fullName,
      "Email": formData.email,
      "Education Level": formData.educationLevel,
      "Academic Performance": formData.academicPerformance,
      "Skills": skillsCombined,
      "Certifications": formData.certifications,
      "Do you prefer working with data, people, or ideas?": formData.workPreference,
      "How do you approach solving complex problems?": formData.problemSolving,
      "Do you thrive better in a structured or flexible environment?": formData.environmentPreference,
      "Do you prefer working independently or in a team?": formData.teamworkPreference,
      "Do you learn best through practice, observation, or theory?": formData.learningStyle,
      "Interests": interestsCombined,
      "Extra-Curricular Activities": formData.extraCurricular,
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-8">
        <div
          className="bg-linear-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-500"
          style={{ width: `${(currentPage / 4) * 100}%` }}
        ></div>
      </div>
      <p className="text-sm text-center text-gray-600">Step {currentPage} of 4</p>

      {/* PAGE 1: Personal & Education */}
      {currentPage === 1 && (
        <div className="space-y-6 animate-fadeIn">
          <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Let's Get Started! 👋
            </h2>
            <p className="text-gray-700">
              Tell us about yourself and your educational background.
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Full Name *
            </label>
            <input
              type="text"
              value={formData.fullName}
              onChange={(e) => handleInputChange("fullName", e.target.value)}
              placeholder="e.g., Ayesha Khan"
              className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              This will appear on your recommendation report.
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Email Address *
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange("email", e.target.value)}
              placeholder="you@example.com"
              className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              We'll use this to send you your career report.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Education Level *
              </label>
              <select
                value={formData.educationLevel}
                onChange={(e) => handleInputChange("educationLevel", e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-gray-300 bg-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="">Select education level</option>
                {educationOptions.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Your highest level of education or qualification.
              </p>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Academic Performance
              </label>
              <input
                type="text"
                value={formData.academicPerformance}
                onChange={(e) => handleInputChange("academicPerformance", e.target.value)}
                placeholder="e.g., 3.4 GPA or 82%"
                className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
              <p className="text-xs text-gray-500 mt-1">
                Your GPA or percentage (optional).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* PAGE 2: Work Style & Problem Solving */}
      {currentPage === 2 && (
        <div className="space-y-6 animate-fadeIn">
          <div className="bg-purple-50 border-l-4 border-purple-600 p-4 rounded">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Your Work Style 💼
            </h2>
            <p className="text-gray-700">
              Help us understand how you prefer to work and solve problems.
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              What excites you most? *
            </label>
            <div className="space-y-2">
              {workPrefOptions.map((opt) => (
                <label
                  key={opt}
                  className="flex items-center p-3 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition"
                >
                  <input
                    type="radio"
                    name="workPref"
                    value={opt}
                    checked={formData.workPreference === opt}
                    onChange={(e) => handleInputChange("workPreference", e.target.value)}
                    className="w-4 h-4 accent-blue-600"
                  />
                  <span className="ml-3 font-medium text-gray-700">{opt}</span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Data: Analytics, numbers. | People: Collaboration, communication. |
              Ideas: Innovation, creativity.
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              How do you solve problems? *
            </label>
            <div className="space-y-2">
              {problemSolvingOptions.map((opt) => (
                <label
                  key={opt}
                  className="flex items-center p-3 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-purple-500 hover:bg-purple-50 transition"
                >
                  <input
                    type="radio"
                    name="problemSolving"
                    value={opt}
                    checked={formData.problemSolving === opt}
                    onChange={(e) => handleInputChange("problemSolving", e.target.value)}
                    className="w-4 h-4 accent-purple-600"
                  />
                  <span className="ml-3 font-medium text-gray-700">{opt}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Environment Preference *
              </label>
              <select
                value={formData.environmentPreference}
                onChange={(e) => handleInputChange("environmentPreference", e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-gray-300 bg-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="">Select preference</option>
                {environmentOptions.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Teamwork Style *
              </label>
              <select
                value={formData.teamworkPreference}
                onChange={(e) => handleInputChange("teamworkPreference", e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-gray-300 bg-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="">Select style</option>
                {teamworkOptions.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Learning Style *
            </label>
            <div className="space-y-2">
              {learningStyleOptions.map((opt) => (
                <label
                  key={opt}
                  className="flex items-center p-3 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-green-500 hover:bg-green-50 transition"
                >
                  <input
                    type="radio"
                    name="learningStyle"
                    value={opt}
                    checked={formData.learningStyle === opt}
                    onChange={(e) => handleInputChange("learningStyle", e.target.value)}
                    className="w-4 h-4 accent-green-600"
                  />
                  <span className="ml-3 font-medium text-gray-700">{opt}</span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Practice: Learn by doing. | Observation: Watch & learn. | Theory:
              Understand concepts first.
            </p>
          </div>
        </div>
      )}

      {/* PAGE 3: Skills & Certifications */}
      {currentPage === 3 && (
        <div className="space-y-6 animate-fadeIn">
          <div className="bg-green-50 border-l-4 border-green-600 p-4 rounded">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Your Skills 🎯
            </h2>
            <p className="text-gray-700">
              Select skills you have or want to develop. We've suggested some
              based on your education.
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Select Skills * (Suggested for{" "}
              {formData.educationLevel || "your background"})
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {dynamicSkills.map((skill) => (
                <button
                  key={skill}
                  type="button"
                  onClick={() => toggleSet("skillsSelected", skill)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                    formData.skillsSelected.has(skill)
                      ? "bg-blue-600 text-white"
                      : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                  }`}
                >
                  {skill}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-2">Select at least one skill.</p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Other Skills (Optional)
            </label>
            <input
              type="text"
              value={formData.skillsOther}
              onChange={(e) => handleInputChange("skillsOther", e.target.value)}
              placeholder="e.g., Leadership; Public Speaking"
              className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <p className="text-xs text-gray-500 mt-1">Comma or semicolon separated.</p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Certifications (Optional)
            </label>
            <select
              value={formData.certifications}
              onChange={(e) => handleInputChange("certifications", e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-gray-300 bg-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              <option value="">Select certification</option>
              {dynamicCerts.map((cert) => (
                <option key={cert} value={cert}>
                  {cert}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Certifications you have or plan to earn.
            </p>
          </div>
        </div>
      )}

      {/* PAGE 4: Interests & Summary */}
      {currentPage === 4 && (
        <div className="space-y-6 animate-fadeIn">
          <div className="bg-pink-50 border-l-4 border-pink-600 p-4 rounded">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Your Interests & Final Touch ✨
            </h2>
            <p className="text-gray-700">
              Tell us what you're passionate about and what you do outside of
              work.
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Select Interests * (Based on:{" "}
              {formData.workPreference || "your preference"})
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {dynamicInterests.map((interest) => (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleSet("interestsSelected", interest)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                    formData.interestsSelected.has(interest)
                      ? "bg-purple-600 text-white"
                      : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                  }`}
                >
                  {interest}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Select at least one interest.
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Other Interests (Optional)
            </label>
            <input
              type="text"
              value={formData.interestsOther}
              onChange={(e) => handleInputChange("interestsOther", e.target.value)}
              placeholder="e.g., Photography; Volunteer work"
              className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Extra-Curricular Activities (Optional)
            </label>
            <input
              type="text"
              value={formData.extraCurricular}
              onChange={(e) => handleInputChange("extraCurricular", e.target.value)}
              placeholder="e.g., Hackathons; Coding Club; Sports Team"
              className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <p className="text-xs text-gray-500 mt-1">
              Clubs, competitions, volunteering, etc.
            </p>
          </div>

          {/* Summary */}
          <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
            <h3 className="font-bold text-gray-800 mb-3">Quick Review:</h3>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-gray-600">Name:</span>{" "}
                <span className="font-semibold">{formData.fullName}</span>
              </div>
              <div>
                <span className="text-gray-600">Education:</span>{" "}
                <span className="font-semibold">{formData.educationLevel}</span>
              </div>
              <div>
                <span className="text-gray-600">Work Pref:</span>{" "}
                <span className="font-semibold">{formData.workPreference}</span>
              </div>
              <div>
                <span className="text-gray-600">Skills:</span>{" "}
                <span className="font-semibold">
                  {formData.skillsSelected.size} selected
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Navigation Buttons */}
      <div className="flex justify-between gap-4 pt-6 border-t border-gray-200">
        <button
          type="button"
          onClick={handleBack}
          disabled={currentPage === 1}
          className="px-6 py-3 rounded-xl bg-gray-200 text-gray-800 font-semibold hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          ← Back
        </button>

        {currentPage < 4 ? (
          <button
            type="button"
            onClick={handleNext}
            className="px-6 py-3 rounded-xl bg-linear-to-r from-blue-600 to-purple-600 text-white font-semibold hover:shadow-lg transition"
          >
            Next →
          </button>
        ) : (
          <button
            type="submit"
            disabled={loading || formData.interestsSelected.size === 0}
            className="px-6 py-3 rounded-xl bg-linear-to-r from-green-600 to-emerald-600 text-white font-semibold hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {loading ? "Submitting..." : "Get Recommendation"}
          </button>
        )}
      </div>
    </form>
  );
};

// Main page component
const CareerFormPage = ({ setResult }) => {
  const [loading, setLoading] = useState(false);
  const [formType, setFormType] = useState("form");

  // Use token for authenticated requests and handle 401 gracefully
  const handleFormSubmit = async (formData) => {
    setLoading(true);
    const token = localStorage.getItem("token");
    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(formData),
      });

      if (res.status === 401) {
        alert("Session expired. Please login again.");
        window.location.hash = "#/login";
        return;
      }

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText || "Submission failed");
      }

      const data = await res.json();
      // keep 3s loader before result
      await new Promise((r) => setTimeout(r, 3000));
      setResult?.(data);
      window.location.hash = "#/result";
    } catch (e) {
      console.error(e);
      alert(`Submission failed.\n${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleResumeSubmit = async (file) => {
    if (!file) {
      alert("Please select a resume file (PDF/DOCX).");
      return;
    }
    // Basic client-side validation
    const allowed = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!allowed.includes(file.type)) {
      alert("Only PDF or DOCX resumes are supported.");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      alert("File too large. Max 5 MB.");
      return;
    }

    setLoading(true);
    try {
      const fd = new FormData();
      // IMPORTANT: backend expects "file" not "resume"
      fd.append("file", file);

      const token = localStorage.getItem("token");
      const res = await fetch("http://127.0.0.1:8000/predict-resume", {
        method: "POST",
        body: fd,
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });

      if (res.status === 401) {
        alert("Session expired. Please login again.");
        window.location.hash = "#/login";
        return;
      }

      const text = await res.text();
      if (!res.ok) throw new Error(text || "Upload failed");

      let data;
      try {
        data = JSON.parse(text);
      } catch {
        data = { "Career Rationale": text };
      }

      // keep 3s loader before result
      await new Promise((r) => setTimeout(r, 3000));
      setResult?.(data);
      window.location.hash = "#/result";
    } catch (e) {
      console.error(e);
      alert(`Resume submission failed.\n${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-linear-to-br from-blue-50 via-purple-50 to-pink-50 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 -left-20 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 -right-20 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>
      {loading && <Loader />}
      <div className="relative z-10 px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="max-w-3xl mx-auto mb-8 text-center">
          <h1 className="text-4xl sm:text-5xl font-extrabold bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
            Discover Your Career Path
          </h1>
          <p className="text-gray-600 text-lg">
            Interactive questionnaire powered by AI
          </p>
        </div>
        {/* Toggle */}
        <div className="max-w-3xl mx-auto mb-8 flex justify-center">
          <div className="flex items-center bg-white rounded-full p-1 shadow-lg border border-gray-200">
            <button
              onClick={() => setFormType("form")}
              className={`px-6 py-2 text-sm font-semibold rounded-full transition ${
                formType === "form"
                  ? "bg-blue-600 text-white"
                  : "bg-transparent text-gray-600 hover:bg-gray-100"
              }`}
            >
              Form (4 Pages)
            </button>
            <button
              onClick={() => setFormType("resume")}
              className={`px-6 py-2 text-sm font-semibold rounded-full transition ${
                formType === "resume"
                  ? "bg-blue-600 text-white"
                  : "bg-transparent text-gray-600 hover:bg-gray-100"
              }`}
            >
              Upload Resume
            </button>
          </div>
        </div>

        {/* Form Container */}
        <div className="max-w-3xl mx-auto bg-white/90 backdrop-blur-md rounded-2xl p-8 shadow-xl border border-gray-200">
          {formType === "form" ? (
            <MultiPageCareerForm onSubmit={handleFormSubmit} loading={loading} />
          ) : (
            <ResumeUploadForm onSubmit={handleResumeSubmit} loading={loading} />
          )}
        </div>
      </div>
    </div>
  );
};

export default CareerFormPage;
