// src/pages/Dashboard.jsx
import { Briefcase, FileText, MessageCircle, User } from "lucide-react";
import { useEffect, useState } from "react";
import { pingBackend } from "../Services/api";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const [backendStatus, setBackendStatus] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState(null);

  console.log("Dashboard component mounted, current state:", { backendStatus, isLoading, lastChecked });

  const testBackendConnection = async () => {
    console.log("Manual backend test...");
    setIsLoading(true);
    try {
      const data = await pingBackend();
      console.log("Manual test response:", data);
      setBackendStatus(data.message || "Backend connected successfully!");
      setLastChecked(new Date().toLocaleTimeString());
    } catch (error) {
      console.error("Manual test failed:", error);
      setBackendStatus("Backend connection failed");
      setLastChecked(new Date().toLocaleTimeString());
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const checkBackend = async () => {
      console.log("Starting backend check...");
      try {
        console.log("Calling pingBackend...");
        const data = await pingBackend();
        console.log("Backend response:", data);
        setBackendStatus(data.message || "Backend connected successfully!");
        setLastChecked(new Date().toLocaleTimeString());
      } catch (error) {
        console.error("Backend ping failed:", error);
        console.error("Error details:", {
          message: error.message,
          stack: error.stack,
          response: error.response
        });
        setBackendStatus("Backend connection failed");
      } finally {
        setIsLoading(false);
      }
    };

    // Add a small delay to ensure everything is loaded
    const timer = setTimeout(() => {
      checkBackend();
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isLoading ? 'bg-yellow-400' : backendStatus.includes('failed') ? 'bg-red-400' : 'bg-green-400'}`}></div>
            <span className={`text-sm ${isLoading ? 'text-yellow-600' : backendStatus.includes('failed') ? 'text-red-600' : 'text-green-600'}`}>
              {isLoading ? 'Connecting...' : backendStatus.includes('failed') ? 'Offline' : 'Online'}
            </span>
            {lastChecked && (
              <span className="text-xs text-gray-500">
                Last checked: {lastChecked}
              </span>
            )}
            <button 
              onClick={() => window.location.reload()} 
              className="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Refresh
            </button>
            <button 
              onClick={testBackendConnection} 
              className="px-2 py-1 text-xs bg-green-500 text-white rounded hover:bg-green-600"
            >
              Test Connection
            </button>
          </div>
        </div>
        <p className="text-gray-500">Welcome back! Here's your career overview.</p>
      </div>

      {/* Backend Status Card */}
      <div className={`p-4 rounded-lg border-2 ${isLoading ? 'border-yellow-300 bg-yellow-50' : backendStatus.includes('failed') ? 'border-red-300 bg-red-50' : 'border-green-300 bg-green-50'}`}>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold">Backend Connection Status</h3>
            <p className="text-sm">
              {isLoading ? 'Checking connection...' : backendStatus}
            </p>
            {lastChecked && (
              <p className="text-xs text-gray-600 mt-1">
                Last checked: {lastChecked}
              </p>
            )}
            <p className="text-xs text-gray-500 mt-1">
              Page loaded at: {new Date().toLocaleTimeString()}
            </p>
          </div>
          <div className="flex gap-2">
            <button 
              onClick={testBackendConnection}
              className={`px-3 py-2 rounded text-sm font-medium ${
                isLoading 
                  ? 'bg-yellow-500 text-white cursor-not-allowed' 
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
              disabled={isLoading}
            >
              {isLoading ? 'Testing...' : 'Test Connection'}
            </button>
            <button 
              onClick={() => window.location.reload()}
              className="px-3 py-2 bg-gray-500 text-white rounded text-sm font-medium hover:bg-gray-600"
            >
              Refresh Page
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 text-blue-600 rounded-xl">
              <Briefcase size={24} />
            </div>
            <div> 
              <h3 className="text-lg font-semibold">Jobs Applied</h3>
              <p className="text-2xl font-bold">12</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 text-green-600 rounded-xl">
              <FileText size={24} />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Resumes Uploaded</h3>
              <p className="text-2xl font-bold">3</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 text-purple-600 rounded-xl">
              <MessageCircle size={24} />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Chats with Bot</h3>
              <p className="text-2xl font-bold">24</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-pink-100 text-pink-600 rounded-xl">
              <User size={24} />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Profile Strength</h3>
              <p className="text-2xl font-bold">85%</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Access Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Quick Access to Jobs */}
        <div className="bg-white p-6 rounded-2xl shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">Latest Job Opportunities</h2>
            <Link 
              to="/jobs" 
              className="text-blue-600 hover:text-blue-700 font-medium text-sm"
            >
              View All Jobs →
            </Link>
          </div>
          <p className="text-gray-600 mb-4">
            Discover the latest job openings tailored to your skills and experience.
          </p>
          <div className="grid grid-cols-1 gap-4">
            <div className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition">
              <h3 className="font-semibold text-gray-800">Frontend Developer Intern</h3>
              <p className="text-sm text-gray-600">TechCorp • Remote</p>
              <p className="text-sm text-green-600 font-medium">$25-35/hr</p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition">
              <h3 className="font-semibold text-gray-800">Backend Developer Intern</h3>
              <p className="text-sm text-gray-600">InnovateX • Bangalore</p>
              <p className="text-sm text-green-600 font-medium">₹25,000-35,000/month</p>
            </div>
          </div>
        </div>

        {/* Quick Access to Chatbot */}
        <div className="bg-white p-6 rounded-2xl shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">AI Career Assistant</h2>
            <Link 
              to="/chatbot" 
              className="text-blue-600 hover:text-blue-700 font-medium text-sm"
            >
              Open Chat →
            </Link>
          </div>
          <p className="text-gray-600 mb-4">
            Get instant career advice, job recommendations, and interview tips from our AI assistant.
          </p>
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border border-blue-200">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-gray-800">Chat with AI Assistant</h3>
                <p className="text-sm text-gray-600">Ask about jobs, skills, companies, and career advice</p>
              </div>
              <Link 
                to="/chatbot"
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm font-medium"
              >
                Start Chat
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-6 rounded-2xl shadow">
        <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
        <ul className="space-y-3 text-gray-700">
          <li>✅ Applied for <strong>Frontend Developer</strong> at Google</li>
          <li>📄 Uploaded a new resume</li>
          <li>💬 Practiced mock interview questions</li>
          <li>🔎 Searched jobs related to <strong>React.js</strong></li>
        </ul>
      </div>
    </div>
  );
}
