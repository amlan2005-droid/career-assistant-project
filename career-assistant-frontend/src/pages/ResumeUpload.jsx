import React, { useState } from 'react';
import { uploadResume } from '../Services/api';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf' || selectedFile.type === 'application/msword' || selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please upload a PDF or Word document');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('resume', file);
      
      const response = await uploadResume(formData);
      setAnalysis(response.analysis);
    } catch (err) {
      setError('Failed to upload resume. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">📄 Resume Analysis</h1>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Upload Your Resume</h2>
        
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            Select Resume File (PDF or Word)
          </label>
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {file && (
            <p className="text-sm text-gray-600 mt-2">
              Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
            </p>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {uploading ? 'Analyzing...' : 'Upload & Analyze Resume'}
        </button>
      </div>

      {analysis && (
        <div className="mt-8 space-y-6">
          {/* Analysis Results */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">📊 Resume Analysis Results</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold mb-2">Overall Score</h3>
                <div className="text-3xl font-bold text-blue-600">{analysis.score}/10</div>
              </div>
              
              <div>
                <h3 className="font-semibold mb-2">Experience Level</h3>
                <div className="text-lg">{analysis.experience_years} years</div>
              </div>
            </div>
          </div>

          {/* Skills Found */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold mb-4">🔧 Skills Detected</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.skills_found.map((skill, index) => (
                <span
                  key={index}
                  className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Education */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold mb-2">🎓 Education</h3>
            <p className="text-gray-700">{analysis.education}</p>
          </div>

          {/* Suggestions */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold mb-4">💡 Improvement Suggestions</h3>
            <ul className="space-y-2">
              {analysis.suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-yellow-500 mr-2">•</span>
                  <span className="text-gray-700">{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Job Matches */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold mb-4">🎯 Recommended Job Matches</h3>
            <div className="grid gap-4">
              <div className="p-4 border border-gray-200 rounded-lg">
                <h4 className="font-medium">Frontend Developer Intern</h4>
                <p className="text-sm text-gray-600">TechCorp • Remote</p>
                <p className="text-sm text-green-600">Match: 95%</p>
              </div>
              <div className="p-4 border border-gray-200 rounded-lg">
                <h4 className="font-medium">Full Stack Developer</h4>
                <p className="text-sm text-gray-600">StartupHub • Mumbai</p>
                <p className="text-sm text-green-600">Match: 88%</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
