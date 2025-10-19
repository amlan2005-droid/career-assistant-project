import { useEffect, useState } from "react";
import JobCard from "../components/JobCard"; // card component
import { getAvailableJobs, searchJobs } from "../Services/api";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searching, setSearching] = useState(false);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      console.log("Fetching available jobs...");
      
      // Try to fetch real jobs from API
      const response = await getAvailableJobs();
      console.log("Jobs API response:", response);
      
      if (response && response.jobs) {
        setJobs(response.jobs);
      } else if (response && Array.isArray(response)) {
        setJobs(response);
      } else {
        // Fallback to mock data if API doesn't return expected format
        console.log("Using fallback mock data");
        const mockJobs = [
          {
            id: 1,
            title: "Frontend Developer Intern",
            company: "TechCorp",
            location: "Remote",
            tags: ['React', 'JavaScript', 'HTML/CSS'],
            salary: "$25-35/hr",
            posted: "2 days ago"
          },
          {
            id: 2,
            title: "Backend Developer Intern",
            company: "InnovateX",
            location: "Bangalore",
            tags: ['Python', 'FastAPI', 'SQL'],
            salary: "₹25,000-35,000/month",
            posted: "1 week ago"
          }
        ];
        setJobs(mockJobs);
      }
    } catch (err) {
      console.error("Failed to fetch jobs from API:", err);
      // Fallback to mock data on error
      const mockJobs = [
        {
          id: 1,
          title: "Frontend Developer Intern",
          company: "TechCorp",
          location: "Remote",
          tags: ['React', 'JavaScript', 'HTML/CSS'],
          salary: "$25-35/hr",
          posted: "2 days ago"
        },
        {
          id: 2,
          title: "Backend Developer Intern",
            company: "InnovateX",
            location: "Bangalore",
            tags: ['Python', 'FastAPI', 'SQL'],
            salary: "₹25,000-35,000/month",
            posted: "1 week ago"
          }
        ];
      setJobs(mockJobs);
      setError("Using offline data - API connection failed.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchJobs();
      return;
    }

    try {
      setSearching(true);
      setError(null);
      console.log("Searching jobs with query:", searchQuery);
      
      const response = await searchJobs(searchQuery);
      console.log("Search response:", response);
      
      if (response && response.jobs) {
        setJobs(response.jobs);
      } else if (response && Array.isArray(response)) {
        setJobs(response);
      } else {
        setJobs([]);
        setError("No jobs found for your search.");
      }
    } catch (err) {
      console.error("Search failed:", err);
      setError("Search failed. Please try again.");
      setJobs([]);
    } finally {
      setSearching(false);
    }
  };

  if (loading) return <p className="text-gray-600">Loading jobs...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">Available Jobs</h1>
        
        {/* Search Bar */}
        <div className="flex gap-4 mb-6">
          <input
            type="text"
            placeholder="Search for jobs (e.g., React, Python, Remote)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button
            onClick={handleSearch}
            disabled={searching}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {searching ? 'Searching...' : 'Search'}
          </button>
          {searchQuery && (
            <button
              onClick={() => {
                setSearchQuery("");
                fetchJobs();
              }}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
            >
              Clear
            </button>
          )}
          <button
            onClick={fetchJobs}
            disabled={loading}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Refreshing...' : '🔄 Refresh'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">{error}</p>
        </div>
      )}

      {/* Job Count */}
      {jobs.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-blue-800 font-medium">
            📊 Found {jobs.length} job{jobs.length !== 1 ? 's' : ''}
            {searchQuery && ` matching "${searchQuery}"`}
          </p>
        </div>
      )}

      {/* Jobs List */}
      {jobs.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      ) : !loading && !searching ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No jobs found.</p>
          {searchQuery && (
            <p className="text-gray-400 text-sm mt-2">
              Try adjusting your search terms or browse all available jobs.
            </p>
          )}
        </div>
      ) : null}

      {/* Loading State */}
      {(loading || searching) && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="text-gray-600 mt-2">
            {loading ? 'Loading jobs...' : 'Searching...'}
          </p>
        </div>
      )}
    </div>
  );
}
