import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { uploadResume } from "../Services/api";
import ResumeScoreGauge from "../components/ResumeScoreGauge";

const INDUSTRY_AVG_ADI = 4.5;

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (!token) {
      setError("You are not logged in. Please log in to upload a resume.");
      setTimeout(() => navigate("/login"), 2000);
    }
  }, [navigate]);

  /* ================= ADI UI HELPERS ================= */
  const getAdiStyle = (score) => {
    if (score <= 3)
      return { bar: "bg-red-500", text: "text-red-600", label: "Low Impact" };
    if (score <= 6)
      return {
        bar: "bg-yellow-400",
        text: "text-yellow-600",
        label: "Moderate Impact",
      };
    return {
      bar: "bg-green-500",
      text: "text-green-600",
      label: "High Impact",
    };
  };

  /* ================= FILE CHANGE ================= */
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    const validTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/msword",
    ];

    if (!validTypes.includes(selectedFile.type)) {
      setError("Please upload a PDF or Word document");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError("");
    setAnalysis(null);
  };

  /* ================= UPLOAD ================= */
  const handleUpload = async () => {
    if (!file) {
      setError("Please select a resume first");
      return;
    }

    setUploading(true);
    setError("");
    setAnalysis(null);

    try {
      const response = await uploadResume(file);
      // Support nested analysis or flat response
      const analysisData = response?.analysis ?? response;

      if (!analysisData || typeof analysisData !== "object") {
        throw new Error("Invalid analysis response");
      }

      setAnalysis(analysisData);
    } catch (err) {
      console.error("Upload error:", err);
      setError(
        err?.response?.data?.detail ||
        err?.detail ||
        err?.message ||
        "Resume analysis failed"
      );
    } finally {
      setUploading(false);
    }
  };

  /* ================= SAFE DATA ACCESS ================= */
  const adiScore =
    analysis?.achievement_density_index?.adi_score ??
    analysis?.achievement_density?.adi_score ??
    0;

  const adiUI = getAdiStyle(adiScore);

  /* ================= UI ================= */
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">📄 Resume Intelligence</h1>

      {/* ========= Upload Card ========= */}
      <div className="bg-white p-6 rounded-xl shadow border border-gray-100">
        <h2 className="text-xl font-semibold mb-4">Upload Your Resume</h2>
        <div className="flex flex-col gap-4">
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />

          {file && (
            <p className="text-sm text-gray-600">
              Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
            </p>
          )}

          {error && <p className="text-red-600 text-sm font-medium">{error}</p>}

          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl transition-all disabled:bg-gray-400 disabled:cursor-not-allowed shadow-md"
          >
            {uploading ? "Analyzing resume..." : "Upload & Analyze"}
          </button>
        </div>
      </div>

      {/* ========= Analysis ========= */}
      {analysis && (
        <div className="mt-8 space-y-6">
          <h2 className="text-2xl font-bold text-gray-800">📊 Analysis Results</h2>

          {/* ===== Resume Score + Gauge ===== */}
          <div className="bg-white p-6 rounded-xl shadow flex items-center justify-between border border-gray-100">
            <div>
              <h2 className="font-bold text-lg mb-1">Overall Resume Score</h2>
              <p className="text-gray-500 italic">
                Experience Level: {analysis.experience_level || "Not detected"}
              </p>
            </div>
            <ResumeScoreGauge score={analysis.resume_score || analysis.score || 0} />
          </div>

          {/* ===== Skills ===== */}
          <div className="bg-white p-6 rounded-xl shadow border border-gray-100">
            <h3 className="font-bold mb-4 flex items-center gap-2">
              <span className="text-blue-500">🔧</span> Skills Detected
            </h3>
            <div className="flex flex-wrap gap-2">
              {(analysis.skills || analysis.skills_found || []).map((skill, i) => (
                <span
                  key={i}
                  className="bg-blue-50 text-blue-700 border border-blue-100 px-3 py-1 rounded-full text-sm font-medium"
                >
                  {skill}
                </span>
              ))}
              {(analysis.skills || analysis.skills_found || []).length === 0 && (
                <p className="text-gray-400 text-sm">No specific skills detected.</p>
              )}
            </div>
          </div>

          {/* ===== Strengths / Weaknesses / Suggestions ===== */}
          <div className="grid md:grid-cols-3 gap-6">
            {/* Strengths */}
            <div className="bg-green-50 p-5 rounded-xl border border-green-100">
              <h4 className="font-bold mb-3 text-green-800 flex items-center gap-2">
                ✅ Strengths
              </h4>
              <ul className="text-sm text-green-700 space-y-2">
                {(analysis.strengths || []).map((s, i) => <li key={i}>• {s}</li>)}
                {(analysis.strengths || []).length === 0 && <li>Good overall structure</li>}
              </ul>
            </div>

            {/* Weaknesses */}
            <div className="bg-red-50 p-5 rounded-xl border border-red-100">
              <h4 className="font-bold mb-3 text-red-800 flex items-center gap-2">
                ⚠️ Weaknesses
              </h4>
              <ul className="text-sm text-red-700 space-y-2">
                {(analysis.weaknesses || []).map((w, i) => <li key={i}>• {w}</li>)}
                {(analysis.weaknesses || []).length === 0 && <li>No major weaknesses found</li>}
              </ul>
            </div>

            {/* Suggestions */}
            <div className="bg-blue-50 p-5 rounded-xl border border-blue-100">
              <h4 className="font-bold mb-3 text-blue-800 flex items-center gap-2">
                💡 Suggestions
              </h4>
              <ul className="text-sm text-blue-700 space-y-2">
                {(analysis.suggestions || []).map((s, i) => <li key={i}>• {s}</li>)}
                {(analysis.suggestions || []).length === 0 && <li>Consider adding more quantifiers</li>}
              </ul>
            </div>
          </div>

          {/* ===== Achievement Density Index (ADI) ===== */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-xl text-gray-800">Achievement Density Index</h3>
              <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${adiUI.text} ${adiUI.bar.replace('bg-', 'bg-opacity-20 ')}`}>
                {adiUI.label}
              </span>
            </div>

            <div className="flex items-end gap-2 mb-4">
              <span className="text-5xl font-black text-gray-900">{adiScore}</span>
              <span className="text-gray-400 font-medium mb-1">/ 10</span>
            </div>

            <div className="w-full bg-gray-100 rounded-full h-4 mb-4">
              <div
                className={`h-4 rounded-full transition-all duration-1000 ${adiUI.bar}`}
                style={{ width: `${adiScore * 10}%` }}
              />
            </div>

            <p className="text-sm text-gray-600">
              Industry Standard: <strong>{INDUSTRY_AVG_ADI}/10</strong> •{" "}
              {adiScore >= INDUSTRY_AVG_ADI ? (
                <span className="text-green-600 font-bold">Excellent: Your resume is highly impact-focused!</span>
              ) : (
                <span className="text-yellow-600 font-bold">Room for improvement in highlighting quantifiable results.</span>
              )}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
