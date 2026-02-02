import React, { useState, useEffect } from "react";
import api, { startInterview } from "../Services/api";
import { useNavigate } from "react-router-dom";
import SkillConfidencePanel from "../components/SkillConfidencePanel";

const InterviewSetup = () => {
    const navigate = useNavigate();

    const [domain, setDomain] = useState("python");
    const [domains, setDomains] = useState([]);
    const [skillInsights, setSkillInsights] = useState([]);
    const [domainsLoading, setDomainsLoading] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        setDomainsLoading(true);

        api.get("/interview/domains")
            .then(res => {
                console.log("INTERVIEW SETUP DATA:", res.data);
                const fetchedDomains = res.data.domains || [];
                setDomains(fetchedDomains);
                setSkillInsights(res.data.skill_insights || []);

                if (fetchedDomains.length > 0) {
                    setDomain(fetchedDomains[0]);
                } else {
                    setError("No domains available. Please upload your resume first.");
                }
            })
            .catch(err => {
                console.error("Failed to fetch domains:", err);
                setError("Unable to load domains. Please try again or upload your resume.");
            })
            .finally(() => {
                setDomainsLoading(false);
            });
    }, []);


    const handleStart = async () => {
        setLoading(true);
        setError("");

        try {
            const response = await startInterview({ domain });

            if (!response.session_id) {
                throw new Error("Session ID missing");
            }

            // Pass entire response (session_id, question, question_number) to session page
            navigate(`/interview/${response.session_id}`, { state: response });
        } catch (err) {
            console.error(err);
            const errorMsg =
                err.response?.data?.detail ||
                err.message ||
                "Unable to start interview. Try again.";
            setError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-xl mx-auto p-10 mt-20 bg-white rounded-xl shadow-xl">
            <h1 className="text-3xl font-bold mb-6 text-center">
                Mock Interview Setup
            </h1>

            <div className="mb-6">
                <label className="block font-semibold mb-2">Select Domain</label>
                {domainsLoading ? (
                    <div className="w-full p-3 border rounded-lg bg-gray-50 text-gray-500 text-center">
                        Loading domains...
                    </div>
                ) : domains.length === 0 ? (
                    <div className="w-full p-6 border-2 border-dashed rounded-xl bg-gray-50 text-gray-500 text-center">
                        <p className="mb-4">No domains identified from your resume.</p>
                        <button
                            onClick={() => navigate("/dashboard")}
                            className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors"
                        >
                            Upload/Refresh Resume
                        </button>
                    </div>
                ) : (
                    <select
                        value={domain}
                        onChange={(e) => setDomain(e.target.value)}
                        className="w-full p-3 border rounded-lg"
                    >
                        {domains.map(d => (
                            <option key={d} value={d}>
                                {d.replace("-", " ").toUpperCase()}
                            </option>
                        ))}
                    </select>
                )}
            </div>
            <SkillConfidencePanel skills={skillInsights} />

            {error && <p className="text-red-600 mb-4">{error}</p>}

            <button
                onClick={handleStart}
                disabled={loading || domainsLoading || domains.length === 0}
                className="w-full bg-blue-600 text-white py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
                {loading ? "Starting Interview..." : "Start Interview"}
            </button>
        </div>
    );
};

export default InterviewSetup;
