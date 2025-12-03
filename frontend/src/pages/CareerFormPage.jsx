import React, { useState, useMemo, useEffect } from "react";
import ResumeUploadForm from "../assets/components/ResumeUploadForm";
import Loader from "../assets/components/Loader";

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
  "Diploma": {
    skills: [
      "Excel",
      "SQL",
      "Reporting",
      "React",
      "HTML",
      "CSS",
      "Data Cleaning",
      "Financial Modeling",
    ],
    certs: [
      "FMVA",
      "Google Front-End",
      "AgileBA",
      "Full-Stack Web Dev Certificate",
    ],
  },
  PhD: {
    skills: [
      "Advanced Research",
      "Data Cleaning",
      "Clinical Data Management",
      "Regulatory",
      "SAS",
      "Statistics",
      "Python",
    ],
    certs: ["CDM Cert", "GCP", "Bioinformatics Cert", "AWS ML Specialty"],
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

const EnhancedCareerForm = ({ onSubmit, loading }) => {
  const [fullName, setFullName] = useState("");
  const [educationLevel, setEducationLevel] = useState("");
  const [academicPerformance, setAcademicPerformance] = useState("");
  const [workPreference, setWorkPreference] = useState("");
  const [problemSolving, setProblemSolving] = useState("");
  const [environmentPreference, setEnvironmentPreference] = useState("");
  const [teamworkPreference, setTeamworkPreference] = useState("");
  const [learningStyle, setLearningStyle] = useState("");
  const [extraCurricular, setExtraCurricular] = useState("");
  const [skillsSelected, setSkillsSelected] = useState(new Set());
  const [skillsOther, setSkillsOther] = useState("");
  const [interestsSelected, setInterestsSelected] = useState(new Set());
  const [interestsOther, setInterestsOther] = useState("");
  const [certification, setCertification] = useState("");
  const [certOther, setCertOther] = useState("");

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

  // Dynamic skills/certs from education
  const eduData =
    EDUCATION_MAP[educationLevel] || {
      skills: EDUCATION_MAP["High School Diploma"].skills,
      certs: GENERIC_CERTS,
    };
  const dynamicSkills = eduData.skills;
  const dynamicCerts = [...new Set([...eduData.certs, ...GENERIC_CERTS])];

  // Dynamic interests from work preference
  const dynamicInterests = useMemo(() => {
    if (workPreference === "People") return interestsBase.people;
    if (workPreference === "Ideas") return interestsBase.ideas;
    return interestsBase.data;
  }, [workPreference]);

  // Prune selections when education or work preference changes
  useEffect(() => {
    setSkillsSelected((prev) =>
      new Set([...prev].filter((s) => dynamicSkills.includes(s)))
    );
  }, [educationLevel]);

  useEffect(() => {
    setInterestsSelected((prev) =>
      new Set([...prev].filter((i) => dynamicInterests.includes(i)))
    );
  }, [workPreference]);

  const toggleSet = (setter, set, value) => {
    const next = new Set(set);
    next.has(value) ? next.delete(value) : next.add(value);
    setter(next);
  };

  const submit = (e) => {
    e.preventDefault();
    if (
      !fullName ||
      !educationLevel ||
      !workPreference ||
      !problemSolving ||
      !environmentPreference ||
      !teamworkPreference ||
      !learningStyle
    ) {
      alert("Please fill all required * fields.");
      return;
    }
    const skillsCombined = [
      ...skillsSelected,
      ...(skillsOther
        ? skillsOther.split(/[;,]/).map((x) => x.trim()).filter(Boolean)
        : []),
    ].join("; ");
    const interestsCombined = [
      ...interestsSelected,
      ...(interestsOther
        ? interestsOther.split(/[;,]/).map((x) => x.trim()).filter(Boolean)
        : []),
    ].join("; ");
    const certFinal = certification || (certOther.trim() ? certOther.trim() : "");
    const userId = localStorage.getItem("cp_user_id") || `user_${Date.now()}`;
    localStorage.setItem("cp_user_id", userId);
    onSubmit({
      "User ID": userId,
      "Full Name": fullName,
      "Education Level": educationLevel,
      "Academic Performance": academicPerformance,
      "Skills": skillsCombined,
      "Certifications": certFinal,
      "Do you prefer working with data, people, or ideas?": workPreference,
      "How do you approach solving complex problems?": problemSolving,
      "Do you thrive better in a structured or flexible environment?":
        environmentPreference,
      "Do you prefer working independently or in a team?": teamworkPreference,
      "Do you learn best through practice, observation, or theory?": learningStyle,
      "Interests": interestsCombined,
      "Extra-Curricular Activities": extraCurricular,
    });
  };

  return (
    <form onSubmit={submit} className="space-y-6">
      {/* Personal */}
      <div>
        <label className="block font-semibold mb-1">Full Name *</label>
        <input
          type="text"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="e.g., Ayesha Khan"
          required
        />
        <p className="text-xs text-gray-500 mt-1">
          Your name as it should appear on the report.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block font-semibold mb-1">Education Level *</label>
          <select
            value={educationLevel}
            onChange={(e) => setEducationLevel(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select education level</option>
            {Object.keys(EDUCATION_MAP).map((k) => (
              <option key={k} value={k}>
                {k}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Updates skill & certification suggestions.
          </p>
        </div>

        <div>
          <label className="block font-semibold mb-1">Academic Performance</label>
          <input
            type="text"
            value={academicPerformance}
            onChange={(e) => setAcademicPerformance(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., 3.4 (GPA) or 82%"
          />
          <p className="text-xs text-gray-500 mt-1">
            Provide GPA (e.g., 3.2) or percentage (e.g., 78%).
          </p>
        </div>
      </div>

      {/* Preferences */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block font-semibold mb-1">Work Preference *</label>
          <select
            value={workPreference}
            onChange={(e) => setWorkPreference(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select preference</option>
            {workPrefOptions.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            What excites you most: Data, People, or Ideas?
          </p>
        </div>

        <div>
          <label className="block font-semibold mb-1">Problem-Solving Style *</label>
          <select
            value={problemSolving}
            onChange={(e) => setProblemSolving(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select style</option>
            {problemSolvingOptions.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            How do you naturally approach complex problems?
          </p>
        </div>

        <div>
          <label className="block font-semibold mb-1">Preferred Environment *</label>
          <select
            value={environmentPreference}
            onChange={(e) => setEnvironmentPreference(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select environment</option>
            {environmentOptions.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Do you thrive better with structure or flexibility?
          </p>
        </div>

        <div>
          <label className="block font-semibold mb-1">Teamwork Preference *</label>
          <select
            value={teamworkPreference}
            onChange={(e) => setTeamworkPreference(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select collaboration style</option>
            {teamworkOptions.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Prefer to work independently, in a team, or both?
          </p>
        </div>

        <div>
          <label className="block font-semibold mb-1">Learning Style *</label>
          <select
            value={learningStyle}
            onChange={(e) => setLearningStyle(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="">Select learning style</option>
            {learningStyleOptions.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Do you learn best by Practice, Observation, or Theory?
          </p>
        </div>

        <div>
          <label className="block font-semibold mb-1">Certification (suggested)</label>
          <select
            value={certification}
            onChange={(e) => setCertification(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select certification</option>
            {dynamicCerts.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <input
            value={certOther}
            onChange={(e) => setCertOther(e.target.value)}
            placeholder="Other certification"
            className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Dynamic Skills */}
      <div>
        <div className="flex items-center justify-between">
          <label className="block font-semibold mb-2">
            Skills (dynamic) *
          </label>
          <span className="text-xs text-blue-600">
            {educationLevel || "Select education for suggestions"}
          </span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
          {dynamicSkills.map((s) => (
            <label key={s} className="text-sm flex items-center gap-2">
              <input
                type="checkbox"
                className="accent-blue-600"
                checked={skillsSelected.has(s)}
                onChange={() => toggleSet(setSkillsSelected, skillsSelected, s)}
              />
              <span>{s}</span>
            </label>
          ))}
        </div>
        <input
          value={skillsOther}
          onChange={(e) => setSkillsOther(e.target.value)}
          placeholder="Other skills (comma/semicolon separated)"
          className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Dynamic Interests */}
      <div>
        <div className="flex items-center justify-between">
          <label className="block font-semibold mb-2">
            Interests (based on preference) *
          </label>
          <span className="text-xs text-purple-600">
            {workPreference || "Select work preference"}
          </span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
          {dynamicInterests.map((i) => (
            <label key={i} className="text-sm flex items-center gap-2">
              <input
                type="checkbox"
                className="accent-purple-600"
                checked={interestsSelected.has(i)}
                onChange={() => toggleSet(setInterestsSelected, interestsSelected, i)}
              />
              <span>{i}</span>
            </label>
          ))}
        </div>
        <input
          value={interestsOther}
          onChange={(e) => setInterestsOther(e.target.value)}
          placeholder="Other interests (comma/semicolon separated)"
          className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* Extra-Curricular */}
      <div>
        <label className="block font-semibold mb-1">
          Extra-Curricular Activities (optional)
        </label>
        <input
          type="text"
          value={extraCurricular}
          onChange={(e) => setExtraCurricular(e.target.value)}
          className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="e.g., Coding Club, Research Assistant, Hackathons"
        />
        <p className="text-xs text-gray-500 mt-1">
          Mention clubs, volunteering, competitions, etc.
        </p>
      </div>

      <div className="pt-2">
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-linear-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold px-6 py-3 rounded-xl transition-all duration-300 transform hover:scale-[1.01] shadow-lg"
        >
          {loading ? "Submitting..." : "Get My Career Recommendation"}
        </button>
      </div>
    </form>
  );
};

const CareerFormPage = ({ setResult }) => {
  const [loading, setLoading] = useState(false);
  const [formType, setFormType] = useState("form"); // 'form' or 'resume'

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    const token = localStorage.getItem("token");

    const fetchPromise = fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    }).then(async (response) => {
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error details:", errorText);
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }
      return response.json();
    });

    const timeoutPromise = new Promise((resolve) => setTimeout(resolve, 5000));

    try {
      const [data] = await Promise.all([fetchPromise, timeoutPromise]);
      setResult(data);
      window.location.hash = "#/result";
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("Failed to get prediction. Please check the backend or input data.");
    } finally {
      setLoading(false);
    }
  };

  const handleResumeSubmit = async (file) => {
    setLoading(true);
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", file);

    const fetchPromise = fetch("http://127.0.0.1:8000/predict-resume", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    }).then(async (response) => {
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error details:", errorText);
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }
      return response.json();
    });

    const timeoutPromise = new Promise((resolve) => setTimeout(resolve, 5000));

    try {
      const [data] = await Promise.all([fetchPromise, timeoutPromise]);
      setResult(data);
      window.location.hash = "#/result";
    } catch (error) {
      console.error("Resume prediction failed:", error);
      alert("Failed to get prediction from resume. Please check the file or backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-linear-to-b from-white via-gray-100 to-white text-gray-900 font-poppins flex flex-col items-center justify-center overflow-hidden">
      {loading && <Loader />}
      {/* Background */}
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center opacity-10"></div>
      <div className="absolute inset-0 bg-linear-to-b from-white/80 via-gray-100/70 to-white"></div>

      {/* Page Title */}
      <h1 className="relative z-10 text-4xl sm:text-5xl font-extrabold mb-8 text-center text-blue-600 drop-shadow-[0_0_8px_rgba(59,130,246,0.6)]">
        AI Career Path Finder
      </h1>

      {/* Form Section */}
      <div className="relative z-10 w-full max-w-3xl bg-white/90 backdrop-blur-md border border-gray-200 rounded-2xl p-8 shadow-xl shadow-gray-400/40">
        {/* Toggle */}
        <div className="flex justify-center mb-6">
          <div className="flex items-center bg-gray-100 rounded-full p-1">
            <button
              onClick={() => setFormType("form")}
              className={`px-4 py-2 text-sm font-semibold rounded-full transition-colors ${
                formType === "form"
                  ? "bg-blue-600 text-white"
                  : "bg-transparent text-gray-600 hover:bg-gray-200"
              }`}
            >
              Fill Form
            </button>
            <button
              onClick={() => setFormType("resume")}
              className={`px-4 py-2 text-sm font-semibold rounded-full transition-colors ${
                formType === "resume"
                  ? "bg-blue-600 text-white"
                  : "bg-transparent text-gray-600 hover:bg-gray-200"
              }`}
            >
              Upload Resume
            </button>
          </div>
        </div>

        {formType === "form" ? (
          <EnhancedCareerForm onSubmit={handleFormSubmit} loading={loading} />
        ) : (
          <ResumeUploadForm onSubmit={handleResumeSubmit} loading={loading} />
        )}
      </div>

      {/* Footer */}
      <div className="absolute bottom-4 text-gray-500 text-sm tracking-wide">
        Empowered by{" "}
        <span className="text-blue-600 font-semibold">AI Intelligence</span>
      </div>
    </div>
  );
};

export default CareerFormPage;
