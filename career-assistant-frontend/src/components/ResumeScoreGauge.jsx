import React, { useEffect, useState } from "react";

const INDUSTRY_AVG = 65;

const ResumeScoreGauge = ({ score }) => {
    const [animatedScore, setAnimatedScore] = useState(0);
    const safeScore = Math.min(Math.max(score, 0), 100);

    useEffect(() => {
        let start = 0;
        const step = () => {
            start += 1;
            if (start <= safeScore) {
                setAnimatedScore(start);
                requestAnimationFrame(step);
            }
        };
        step();
    }, [safeScore]);

    const getStatus = () => {
        if (safeScore < 40) return { label: "Weak Resume", color: "red" };
        if (safeScore < 70) return { label: "Average Resume", color: "yellow" };
        return { label: "Strong Resume", color: "green" };
    };

    const status = getStatus();
    const angle = (animatedScore / 100) * 180;
    const circumference = 283;
    const offset = circumference - (circumference * animatedScore) / 100;

    return (
        <div className="flex flex-col items-center bg-white p-6 rounded-2xl shadow-md border">

            {/* Title */}
            <h3 className="text-lg font-bold text-gray-800 mb-4">
                Resume Strength Score
            </h3>

            {/* Gauge */}
            <div className="relative">
                <svg width="240" height="130" viewBox="0 0 240 130">
                    {/* Background Arc */}
                    <path
                        d="M30 110 A90 90 0 0 1 210 110"
                        fill="none"
                        stroke="#e5e7eb"
                        strokeWidth="18"
                    />

                    {/* Gradient Arc */}
                    <defs>
                        <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#ef4444" />
                            <stop offset="50%" stopColor="#facc15" />
                            <stop offset="100%" stopColor="#22c55e" />
                        </linearGradient>
                    </defs>

                    <path
                        d="M30 110 A90 90 0 0 1 210 110"
                        fill="none"
                        stroke="url(#scoreGradient)"
                        strokeWidth="18"
                        strokeDasharray={circumference}
                        strokeDashoffset={offset}
                        strokeLinecap="round"
                        style={{ transition: "stroke-dashoffset 1s ease" }}
                    />

                    {/* Needle */}
                    <line
                        x1="120"
                        y1="110"
                        x2={120 + 75 * Math.cos((Math.PI * (180 - angle)) / 180)}
                        y2={110 - 75 * Math.sin((Math.PI * (180 - angle)) / 180)}
                        stroke="#111827"
                        strokeWidth="3"
                    />

                    <circle cx="120" cy="110" r="5" fill="#111827" />
                </svg>

                {/* Score */}
                <div className="absolute inset-x-0 bottom-4 text-center">
                    <span className="text-4xl font-black text-gray-900">
                        {animatedScore}
                    </span>
                    <span className="text-gray-400 text-sm"> / 100</span>
                </div>
            </div>

            {/* Status Badge */}
            <span
                className={`mt-4 px-4 py-1 rounded-full text-sm font-semibold ${status.color === "red"
                        ? "bg-red-100 text-red-700"
                        : status.color === "yellow"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-green-100 text-green-700"
                    }`}
            >
                {status.label}
            </span>

            {/* Industry Comparison */}
            <div className="mt-4 text-sm text-gray-600">
                Industry Avg:{" "}
                <span className="font-semibold">{INDUSTRY_AVG}</span>{" "}
                {safeScore >= INDUSTRY_AVG ? "Above Avg" : "Below Avg"}
            </div>
        </div>
    );
};

export default ResumeScoreGauge;
