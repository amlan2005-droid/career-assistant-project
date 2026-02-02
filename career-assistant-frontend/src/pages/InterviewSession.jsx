import React, { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import api from "../Services/api";
import PostInterviewReport from "../components/PostInterviewReport";

const InterviewSession = () => {
    const { sessionId } = useParams();
    const location = useLocation();
    const navigate = useNavigate();

    // Init state from navigation state (passed from Setup page)
    const [question, setQuestion] = useState(location.state?.question || "Loading...");
    const [questionNumber, setQuestionNumber] = useState(location.state?.question_number || 1);
    const [difficulty, setDifficulty] = useState(location.state?.difficulty || "Medium");
    const [answer, setAnswer] = useState("");
    const [feedback, setFeedback] = useState(null);
    const [interviewFinished, setInterviewFinished] = useState(false);
    const [report, setReport] = useState(null);
    const [listening, setListening] = useState(false);

    // Speak initial question on mount if available
    useEffect(() => {
        if (location.state?.question) {
            speak(location.state.question);
        }
    }, [location.state]);

    // ---------------- AI VOICE ----------------
    const speak = (text) => {
        if (!text) return;
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 1;
        utterance.pitch = 1;
        window.speechSynthesis.speak(utterance);
    };

    // ---------------- SPEECH RECOGNITION ----------------
    const startListening = () => {
        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) return alert("Speech Recognition not supported!");

        const recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.start();
        setListening(true);

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setAnswer(transcript);
            setListening(false);
        };

        recognition.onerror = () => setListening(false);
    };

    // ---------------- SUBMIT ANSWER ----------------
    const submitAnswer = async () => {
        if (!answer) return alert("Please answer first");

        try {
            // Updated API endpoint to use correct axios instance if possible, 
            // but keeping axios import for now as per original file.
            // Using absolute path or relying on proxy? The original used axios.post
            // The Setup page used 'startInterview' from '../Services/api'.
            // Prefer using the 'api' service if possible, but staying consistent with local file first.
            // Wait, previous file imported 'axios'. The Setup page uses services.
            // I should stick to the requested change only, which is fixing usage.
            // However, to be safe, I will continue using axios as in the original file, 
            // assuming baseURL is set or it's relative.
            // Wait, api.js has baseURL set. Simple axios calls might fail if not configured.
            // The original file used `axios.post("/interview/start"...)`.
            // If that was working (or supposed to work), I'll stick to it.
            // Actually, better to use the api service if I can see it. 
            // I'll stick to 'axios' for now to minimize diffs, but correct the logic.

            // Note: Use the api service if you want the interceptors/base url.
            // The user said: "Your backend is fine".

            const res = await api.post("/interview/answer", {
                session_id: sessionId,
                answer,
            });

            if (res.data.interview_finished) {
                setInterviewFinished(true);
                setFeedback({
                    final_score: res.data.final_score_percentage,
                    message: res.data.message,
                });
                setReport(res.data.report);

                speak(`Interview completed. Your final score is ${res.data.final_score_percentage} percent.`);
            } else {
                setQuestion(res.data.question);
                setQuestionNumber(res.data.question_number);
                if (res.data.difficulty) setDifficulty(res.data.difficulty);
                setAnswer("");
                setFeedback(null);

                speak(res.data.question);
            }
        } catch (err) {
            console.error(err);
            alert("Error submitting answer");
        }
    };

    if (!sessionId) {
        return <div className="p-10 text-center">No Session ID found. Please start over.</div>;
    }

    return (
        <div className="p-6 max-w-xl mx-auto bg-white shadow-xl rounded-xl">
            <h2 className="text-xl font-bold mb-4">AI Interviewer</h2>

            {!interviewFinished ? (
                <>
                    <p className="text-sm text-gray-500 mb-2">
                        Difficulty: <b>{difficulty.toUpperCase()}</b>
                    </p>
                    <p className="font-semibold mb-2">Question {questionNumber}:</p>
                    <div className="bg-gray-100 p-4 rounded mb-4 text-lg">
                        {question}
                    </div>

                    <textarea
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        className="w-full p-2 border rounded mb-4 h-32"
                        placeholder="Your spoken answer will appear here..."
                    />

                    <div className="flex gap-3 mb-4">
                        <button
                            onClick={startListening}
                            className={`px-4 py-2 rounded text-white ${listening ? 'bg-red-500' : 'bg-blue-600'}`}
                        >
                            {listening ? " Stop Listening" : " Start Speaking"}
                        </button>

                        <button
                            onClick={submitAnswer}
                            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                        >
                            Submit Answer
                        </button>
                    </div>
                </>
            ) : (
                <div className="space-y-8">
                    <div className="p-8 bg-white rounded-3xl border border-gray-100 shadow-xl text-center">
                        <h3 className="font-black text-4xl text-gray-900 mb-2">Interview Finished ✅</h3>
                        <p className="text-gray-500 mb-6">{feedback?.message}</p>

                        <div className="inline-flex items-center gap-4 bg-indigo-50 px-6 py-3 rounded-2xl mb-6">
                            <span className="text-indigo-600 font-bold">Final Score</span>
                            <span className="text-3xl font-black text-indigo-700">{feedback?.final_score}%</span>
                        </div>

                        <div className="flex justify-center gap-4">
                            <button
                                onClick={() => navigate('/interview-prep')}
                                className="px-6 py-3 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200"
                            >
                                Start New Interview
                            </button>
                            <button
                                onClick={() => navigate('/dashboard')}
                                className="px-6 py-3 bg-white text-gray-700 font-bold rounded-xl border border-gray-200 hover:bg-gray-50 transition-colors"
                            >
                                Back to Dashboard
                            </button>
                        </div>
                    </div>

                    {report && <PostInterviewReport report={report} />}
                </div>
            )}
        </div>
    );
};

export default InterviewSession;
