import React from "react";

export default function ResultCard({ result, onBack }) {
  const styles = {
    card: {
      background: "linear-gradient(145deg, #0d0d0d, #1a1a1a)",
      color: "#e5e5e5",
      padding: "2rem",
      borderRadius: "1.5rem",
      boxShadow: "0 0 25px rgba(0,0,0,0.6)",
      width: "100%",
      maxWidth: "700px",
      margin: "2rem auto",
      border: "1px solid #2a2a2a",
      backdropFilter: "blur(10px)",
      animation: "fadeIn 0.6s ease-in-out",
      fontFamily: "Poppins, sans-serif",
    },
    title: {
      textAlign: "center",
      fontSize: "1.8rem",
      color: "#4da3ff",
      marginBottom: "1.5rem",
      fontWeight: "700",
    },
    content: {
      lineHeight: "1.6",
      color: "#ccc",
    },
    label: {
      color: "#4da3ff",
      fontWeight: "600",
    },
    button: {
      width: "100%",
      padding: "0.9rem",
      background: "#007bff",
      color: "white",
      border: "none",
      borderRadius: "0.8rem",
      fontSize: "1rem",
      fontWeight: "600",
      cursor: "pointer",
      marginTop: "1.5rem",
      transition: "all 0.3s ease",
    },
  };

  return (
    <div style={styles.card}>
      <h2 style={styles.title}>🎯 Recommended Career</h2>

      <div style={styles.content}>
        <p>
          <span style={styles.label}>Career Domain:</span>{" "}
          {result["Best-Fit Career Domain"]}
        </p>
        <p>
          <span style={styles.label}>Confidence Score:</span>{" "}
          {result["Confidence Score"]}
        </p>
        <p>
          <span style={styles.label}>Rationale:</span>{" "}
          {result["Career Rationale"]}
        </p>
        <p>
          <span style={styles.label}>5-Year Growth Roadmap:</span>{" "}
          {result["5-Year Career Growth Roadmap"]}
        </p>
        <p>
          <span style={styles.label}>Skill Gap:</span>{" "}
          {result["Skill Gap Analysis"]}
        </p>
        <p>
          <span style={styles.label}>Recommended Tools/Courses:</span>{" "}
          {result["Recommended Tools, Courses, and Certifications"]}
        </p>
        <p>
          <span style={styles.label}>Backup Option:</span>{" "}
          {result["Alternative/Backup Career Option"]}
        </p>
        <p>
          <span style={styles.label}>Behavioral Insight:</span>{" "}
          {result["Behavioral Insight"]}
        </p>
      </div>

      <button
        onClick={onBack}
        style={styles.button}
        onMouseEnter={(e) => {
          e.target.style.background = "#0063cc";
          e.target.style.transform = "scale(1.03)";
        }}
        onMouseLeave={(e) => {
          e.target.style.background = "#007bff";
          e.target.style.transform = "scale(1)";
        }}
      >
        🔙 Go Back
      </button>
    </div>
  );
}
