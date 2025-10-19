import React, { useState } from "react";
import { uploadResume } from "../Services/api";

const OnboardingForm = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState(null); // 'success' or 'error'

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setMessage("");
    setMessageType(null);
    
    // Validate file type
    if (selectedFile) {
      const validTypes = ['.pdf', '.doc', '.docx'];
      const fileExtension = selectedFile.name.toLowerCase().substring(selectedFile.name.lastIndexOf('.'));
      if (!validTypes.includes(fileExtension)) {
        setMessage("Please select a valid file type (.pdf, .doc, .docx)");
        setMessageType("error");
        setFile(null);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please upload a resume file.");
      setMessageType("error");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    try {
      setUploading(true);
      setMessage("");
      setMessageType(null);
      await uploadResume(formData);
      setMessage("Resume uploaded successfully!");
      setMessageType("success");
      setFile(null);
      // Reset file input
      e.target.reset();
    } catch (err) {
      console.error(err);
      setMessage("Failed to upload resume. Please try again.");
      setMessageType("error");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-center text-blue-700">Upload Your Resume</h2>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="resume" className="block text-sm font-medium text-gray-700 mb-2">
            Select Resume File
          </label>
          <input
            id="resume"
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
            className="block w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={uploading}
          />
          <p className="text-xs text-gray-500 mt-1">
            Accepted formats: PDF, DOC, DOCX
          </p>
        </div>

        <button
          type="submit"
          disabled={uploading || !file}
          className={`w-full font-semibold py-2 px-4 rounded-lg transition-colors ${
            uploading || !file
              ? "bg-gray-400 cursor-not-allowed text-gray-600"
              : "bg-blue-500 hover:bg-blue-600 text-white"
          }`}
        >
          {uploading ? "Uploading..." : "Upload Resume"}
        </button>
      </form>

      {message && (
        <div className={`mt-4 p-3 rounded-lg text-center text-sm ${
          messageType === "success" 
            ? "bg-green-100 text-green-800 border border-green-200" 
            : "bg-red-100 text-red-800 border border-red-200"
        }`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default OnboardingForm;
