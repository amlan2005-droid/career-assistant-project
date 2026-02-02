import { useEffect, useState } from "react";
import JobCard from "../components/JobCard";
import { getAvailableJobs, searchJobs } from "../Services/api";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState(null);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const data = await getAvailableJobs();
      setJobs(data);
    } catch (err) {
      setError("Failed to load jobs");
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
      const data = await searchJobs(searchQuery);
      setJobs(data);
    } catch (err) {
      setError("Search failed. Please try again.");
      setJobs([]);
    } finally {
      setSearching(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Explore Jobs</h1>

      {/* Search */}
      <div className="flex gap-3">
        <input
          className="flex-1 border rounded-lg px-4 py-2"
          placeholder="Search jobs (React, Python, AWS...)"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />

        <button
          onClick={handleSearch}
          disabled={searching}
          className="bg-blue-600 text-white px-5 py-2 rounded-lg"
        >
          {searching ? "Searching..." : "Search"}
        </button>
      </div>

      {error && <p className="text-red-500">{error}</p>}

      {loading ? (
        <p>Loading jobs...</p>
      ) : jobs.length > 0 ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      ) : (
        <p>No jobs found</p>
      )}
    </div>
  );
}
