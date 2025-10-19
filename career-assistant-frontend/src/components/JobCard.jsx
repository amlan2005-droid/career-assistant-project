// src/components/JobCard.jsx
import React from "react";
import PropTypes from "prop-types";

const JobCard = ({ job }) => {
  const {
    title = "Untitled Role",
    company = "Unknown Company",
    location = "Remote",
    link = null,
    salary = "Not specified",
    posted = "Recently",
    tags = [],
    type = "Full-time",
    experience = "Not specified",
    description = "No description available"
  } = job || {};

  return (
    <div className="bg-white shadow-md rounded-2xl p-6 hover:shadow-lg transition border border-gray-100">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
          <p className="text-gray-600 font-medium">{company}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
          type === 'Internship' ? 'bg-green-100 text-green-800' :
          type === 'Full-time' ? 'bg-blue-100 text-blue-800' :
          'bg-purple-100 text-purple-800'
        }`}>
          {type}
        </span>
      </div>

      {/* Location and Experience */}
      <div className="flex items-center gap-4 mb-3 text-sm text-gray-500">
        <span className="flex items-center gap-1">
          📍 {location}
        </span>
        <span className="flex items-center gap-1">
          👤 {experience}
        </span>
      </div>

      {/* Salary and Posted */}
      <div className="flex items-center gap-4 mb-4 text-sm">
        <span className="text-green-600 font-medium">💰 {salary}</span>
        <span className="text-gray-500">📅 {posted}</span>
      </div>

      {/* Description */}
      <p className="text-gray-700 text-sm mb-4 line-clamp-3">{description}</p>

      {/* Tags */}
      {tags && tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {tags.map((tag, index) => (
            <span
              key={index}
              className="bg-blue-50 text-blue-700 text-xs px-2 py-1 rounded-full border border-blue-200"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Action Button */}
      <div className="mt-4">
        {link ? (
          <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="w-full text-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-200"
          >
            View Job →
          </a>
        ) : (
          <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-200">
            Apply Now
          </button>
        )}
      </div>
    </div>
  );
};

JobCard.propTypes = {
  job: PropTypes.shape({
    title: PropTypes.string,
    company: PropTypes.string,
    location: PropTypes.string,
    link: PropTypes.string,
    salary: PropTypes.string,
    posted: PropTypes.string,
    tags: PropTypes.arrayOf(PropTypes.string),
    type: PropTypes.string,
    experience: PropTypes.string,
    description: PropTypes.string,
  }),
};

export default JobCard;
