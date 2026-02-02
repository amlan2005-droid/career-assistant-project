import React, { useState } from "react";
import { uploadResume } from "../Services/api";
import ResumeScoreGauge from "../components/ResumeScoreGauge";

const INDUSTRY_AVG_ADI = 4.5;

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

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
    ];

    if (!validTypes.includes(selectedFile.type)) {
      setError("Please upload a PDF or DOCX file");
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

      const analysisData = response?.analysis ?? response;

      if (!analysisData || typeof analysisData !== "object") {
        throw new Error("Invalid analysis response");
      }

      setAnalysis(analysisData);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
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
      <h1 className="text-3xl font-bold mb-6"> Resume Intelligence</h1>

      {/* ========= Upload Card ========= */}
      <div className="bg-white p-6 rounded-xl shadow">
        <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />

        {file && <p className="text-sm text-gray-600 mt-2">{file.name}</p>}
        {error && <p className="text-red-600 mt-3">{error}</p>}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg disabled:bg-gray-400"
        >
          {uploading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </div>

      {/* ========= Analysis ========= */}
      {analysis && (
        <div className="mt-8 space-y-6">
          {/* ===== Resume Score + Gauge ===== */}
          <div className="bg-white p-6 rounded-xl shadow flex items-center justify-between">
            <div>
              <h2 className="font-bold mb-1">Resume Score</h2>
              <p className="text-gray-600">
                Experience: {analysis.experience_level}
              </p>
            </div>

            <ResumeScoreGauge score={analysis.resume_score} />
          </div>

          {/* ===== Skills ===== */}
          {analysis.skills?.length > 0 && (
            <div className="bg-white p-6 rounded-xl shadow">
              <h3 className="font-bold mb-3"> Skills Detected</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.skills.map((skill, i) => (
                  <span
                    key={i}
                    className="bg-blue-100 px-3 py-1 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* ===== Strengths / Weaknesses / Suggestions ===== */}
          <div className="grid md:grid-cols-3 gap-4">
            {analysis.strengths?.length > 0 && (
              <div className="bg-green-50 p-4 rounded-xl shadow border border-green-200">
                <h4 className="font-bold mb-2 text-green-700"> Strengths</h4>
                {analysis.strengths.slice(0, 2).map((s, i) => (
                  <p key={i}>• {s}</p>
                ))}
              </div>
            )}

            {analysis.weaknesses?.length > 0 && (
              <div className="bg-red-50 p-4 rounded-xl shadow border border-red-200">
                <h4 className="font-bold mb-2 text-red-700"> Weaknesses</h4>
                {analysis.weaknesses.slice(0, 2).map((w, i) => (
                  <p key={i}>• {w}</p>
                ))}
              </div>
            )}

            {analysis.suggestions?.length > 0 && (
              <div className="bg-blue-50 p-4 rounded-xl shadow border border-blue-200">
                <h4 className="font-bold mb-2 text-blue-700"> Suggestions</h4>
                {analysis.suggestions.slice(0, 2).map((s, i) => (
                  <p key={i}>• {s}</p>
                ))}
              </div>
            )}
          </div>

          {/* ===== ADI ===== */}
          <div className="bg-white p-6 rounded-2xl shadow">
            <div className="flex justify-between mb-2">
              <h3 className="font-bold">Achievement Density Index</h3>
              <span className={`${adiUI.text} font-semibold`}>
                {adiUI.label}
              </span>
            </div>

            <div className="text-4xl font-black mb-2">{adiScore}/10</div>

            <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
              <div
                className={`h-3 rounded-full ${adiUI.bar}`}
                style={{ width: `${adiScore * 10}%` }}
              />
            </div>

            <p className="text-sm text-gray-600">
              Industry Avg: {INDUSTRY_AVG_ADI}/10 •{" "}
              {adiScore >= INDUSTRY_AVG_ADI ? "Above" : "Below"} Average
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
