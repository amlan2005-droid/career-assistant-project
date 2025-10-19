import React from 'react';
import PropTypes from 'prop-types';

const JobListing = ({ title, company, location, tags }) => {
  return (
    <div className="bg-white shadow-md rounded-xl p-4 mb-4 border border-gray-200">
      <h3 className="text-xl font-bold text-gray-800">{title}</h3>
      <p className="text-gray-700">{company} - {location}</p>
      {tags && tags.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-2">
          {tags.map((tag) => (
            <span
              key={tag}  // Better to use a unique identifier if available
              className="bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

JobListing.propTypes = {
  title: PropTypes.string.isRequired,
  company: PropTypes.string.isRequired,
  location: PropTypes.string.isRequired,
  tags: PropTypes.arrayOf(PropTypes.string),
};

JobListing.defaultProps = {
  tags: [],
};

export default JobListing;