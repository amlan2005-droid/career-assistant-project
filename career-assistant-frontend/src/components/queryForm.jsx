import React, { useState } from "react";
import API from "../Services/api";
import PropTypes from "prop-types";

const QueryForm = ({ maxLength = 500 }) => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!query.trim()) {
      setError("Please enter a question");
      return;
    }

    setLoading(true);
    setResponse("");

    try {
      const res = await API.post("/query", { question: query });
      setResponse(res.data.answer || "No response received.");
    } catch (err) {
      console.error("API Error:", err);
      setError(
        err.response?.data?.message || 
        "Failed to get response. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Ask a Question</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
            Your Question
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            maxLength={maxLength}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Type your question here..."
            disabled={loading}
          />
          <div className="text-sm text-gray-500 mt-1">
            {query.length}/{maxLength} characters
          </div>
        </div>

        {error && (
          <div className="text-red-600 text-sm bg-red-50 p-3 rounded-md">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !query.trim()}
          className={`w-full py-2 px-4 rounded-md font-medium ${
            loading || !query.trim()
              ? "bg-gray-400 cursor-not-allowed text-gray-600"
              : "bg-blue-600 hover:bg-blue-700 text-white"
          }`}
        >
          {loading ? "Processing..." : "Submit Question"}
        </button>
      </form>

      {response && (
        <div className="mt-6 p-4 bg-gray-50 rounded-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Response:</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{response}</p>
        </div>
      )}
    </div>
  );
};

QueryForm.propTypes = {
  maxLength: PropTypes.number,
};

QueryForm.defaultProps = {
  maxLength: 500,
};

export default QueryForm;