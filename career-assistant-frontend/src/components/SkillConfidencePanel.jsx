import React from "react";

const levelColor = {
    high: "bg-green-500",
    medium: "bg-yellow-500",
    low: "bg-red-500"
};

const SkillConfidencePanel = ({ skills }) => {
    if (!skills || skills.length === 0) return null;

    return (
        <div className="bg-white shadow-lg rounded-xl p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">
                Interview Preparation Insights
            </h2>

            <p className="text-gray-600 text-sm mb-4">
                Based on your resume, the interviewer will focus on these areas.
            </p>

            <div className="space-y-4">
                {skills.map((skill, index) => (
                    <div key={index}>
                        <div className="flex justify-between mb-1">
                            <span className="font-medium">{skill.name}</span>
                            <span className="text-sm text-gray-600">
                                {Math.round(skill.confidence * 100)}% ·{" "}
                                <b className="capitalize">{skill.level}</b>
                            </span>
                        </div>

                        <div className="w-full bg-gray-200 rounded-full h-3">
                            <div
                                className={`h-3 rounded-full transition-all duration-700 ${levelColor[skill.level]}`}
                                style={{ width: `${skill.confidence * 100}%` }}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SkillConfidencePanel;
