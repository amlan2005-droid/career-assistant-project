// src/components/FeedbackCard.jsx
import React from 'react';

const FeedbackCard = ({ question, answer, feedback, score }) => {
  return (
    <div className="bg-white shadow-md rounded-2xl p-5 mb-4 border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">🗂️ Question</h3>
      <p className="text-gray-700 mb-4">{question}</p>

      <h4 className="text-md font-semibold text-gray-800 mb-2">🗣️ Your Answer</h4>
      <p className="text-gray-600 mb-4">{answer}</p>

      <h4 className="text-md font-semibold text-gray-800 mb-2">💬 Feedback</h4>
      <p className="text-gray-600 mb-4">{feedback}</p>

      {score !== undefined && (
        <div className="text-right mt-4">
          <span className="inline-block bg-green-100 text-green-800 text-sm font-medium px-3 py-1 rounded-full">
            Score: {score}/10
          </span>
        </div>
      )}
    </div>
  );
};

export default FeedbackCard;
