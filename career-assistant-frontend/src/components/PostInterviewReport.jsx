import React from 'react';
import { Trophy, Target, BarChart, Info } from 'lucide-react';

/**
 * PostInterviewReport Component
 * 
 * A premium analytics dashboard shown after an interview.
 * It compares resume confidence with actual interview performance.
 * 
 * @param {Object} report - The report data
 * @param {Array} report.skills - Array of skill objects { name, resume_confidence, interview_score, feedback }
 */
const PostInterviewReport = ({ report }) => {
    if (!report || !report.skills) return null;

    return (
        <div className="bg-white/80 backdrop-blur-md p-8 rounded-3xl shadow-2xl border border-gray-100 max-w-4xl mx-auto animate-fadeIn">
            <style>
                {`
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes slideIn {
                    from { opacity: 0; transform: translateX(-20px); }
                    to { opacity: 1; transform: translateX(0); }
                }
                @keyframes growWidth {
                    from { width: 0; }
                    to { width: var(--final-width); }
                }
                .animate-fadeIn {
                    animation: fadeIn 0.6s ease-out forwards;
                }
                .animate-slideIn {
                    animation: slideIn 0.5s ease-out forwards;
                }
                .animate-growWidth {
                    animation: growWidth 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
                }
                `}
            </style>

            <div className="flex items-center gap-3 mb-8">
                <div className="p-3 bg-indigo-100 rounded-2xl">
                    <BarChart className="w-8 h-8 text-indigo-600" />
                </div>
                <div>
                    <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                        Interview Analysis
                    </h2>
                    <p className="text-gray-500">Deep dive into your skill performance and resume alignment</p>
                </div>
            </div>

            <div className="grid gap-6">
                {report.skills.map((skill, index) => (
                    <div
                        key={index}
                        className="group bg-white p-6 rounded-2xl border border-gray-50 hover:border-indigo-100 hover:shadow-lg transition-all duration-300 animate-slideIn"
                        style={{ animationDelay: `${index * 0.15}s`, opacity: 0, animationFillMode: 'forwards' }}
                    >
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 flex items-center justify-center bg-gray-50 rounded-xl group-hover:bg-indigo-50 transition-colors">
                                    <Target className="w-5 h-5 text-gray-500 group-hover:text-indigo-600" />
                                </div>
                                <h3 className="text-xl font-bold text-gray-800">{skill.name}</h3>
                            </div>

                            <div className="flex gap-4">
                                <ScoreBadge
                                    label="Resume Confidence"
                                    score={skill.resume_confidence}
                                    color="blue"
                                />
                                <ScoreBadge
                                    label="Interview Score"
                                    score={skill.interview_score}
                                    color="emerald"
                                />
                            </div>
                        </div>

                        {/* Progress Bars Comparison */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
                            <ProgressBar
                                label="Resume alignment"
                                value={parseFloat(skill.resume_confidence)}
                                color="bg-blue-500"
                                delay={index * 0.15 + 0.3}
                            />
                            <ProgressBar
                                label="Interview demonstration"
                                value={parseFloat(skill.interview_score)}
                                color="bg-emerald-500"
                                delay={index * 0.15 + 0.45}
                            />
                        </div>

                        {/* Insight Section */}
                        <div className="bg-slate-50 rounded-xl p-4 flex gap-3 border border-slate-100">
                            <div className="flex-shrink-0 mt-1">
                                <Info className="w-5 h-5 text-indigo-500" />
                            </div>
                            <div>
                                <p className="text-sm font-semibold text-slate-700 mb-1"> AI Insight</p>
                                <p className="text-slate-600 text-sm leading-relaxed italic">
                                    "{skill.feedback}"
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Performance Summary Footer */}
            <div className="mt-10 p-6 bg-gradient-to-br from-indigo-600 to-purple-700 rounded-2xl text-white">
                <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                    <div className="flex items-center gap-4">
                        <div className="p-4 bg-white/20 backdrop-blur-sm rounded-full">
                            <Trophy className="w-8 h-8" />
                        </div>
                        <div>
                            <h4 className="text-xl font-bold">Overall Performance</h4>
                            <p className="text-indigo-100 text-sm">Based on {report.skills.length} core competencies evaluated</p>
                        </div>
                    </div>
                    <button className="px-8 py-3 bg-white text-indigo-600 font-bold rounded-xl shadow-xl hover:bg-indigo-50 transition-colors">
                        Download Full PDF
                    </button>
                </div>
            </div>
        </div>
    );
};

const ScoreBadge = ({ label, score, color }) => (
    <div className="text-right">
        <p className="text-[10px] uppercase tracking-wider text-gray-400 font-bold leading-none mb-1">{label}</p>
        <p className={`text-lg font-black ${color === 'blue' ? 'text-blue-600' : 'text-emerald-600'}`}>
            {score}
        </p>
    </div>
);

const ProgressBar = ({ label, value, color, delay }) => (
    <div>
        <div className="flex justify-between mb-1.5">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-tight">{label}</span>
            <span className="text-xs font-bold text-gray-700">{value}%</span>
        </div>
        <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
            <div
                className={`h-full ${color} rounded-full animate-growWidth`}
                style={{
                    '--final-width': `${value}%`,
                    width: 0,
                    animationDelay: `${delay}s`,
                    animationFillMode: 'forwards'
                }}
            />
        </div>
    </div>
);

export default PostInterviewReport;
