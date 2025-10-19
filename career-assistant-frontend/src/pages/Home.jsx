import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center px-6 py-12 max-w-2xl">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
         Welcome to Career Champ!
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Your personal career assistant – get resume analysis, job matches, mock interviews, and AI-powered career advice. All in one place.
        </p>

        <div className="text-center">
          <p className="text-gray-500 mb-4">
            Use the navigation menu above to explore all features
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/dashboard">
              <button className="bg-blue-600 text-white px-6 py-3 rounded-xl text-sm font-semibold hover:bg-blue-700 transition">
                Go to Dashboard
              </button>
            </Link>
            <Link to="/jobs">
              <button className="bg-gray-200 text-gray-800 px-6 py-3 rounded-xl text-sm font-semibold hover:bg-gray-300 transition">
                Explore Jobs
              </button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;