import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import FeedbackCard from '../components/FeedbackCard';
import { startInterview, submitAnswer as apiSubmitAnswer, getInterviewDomains } from '../Services/api';

const InterviewPrep = () => {
  const [selectedCategory, setSelectedCategory] = useState('python'); // Default to python, backend expects specific domains
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [score, setScore] = useState(null);
  const [feedbackMsg, setFeedbackMsg] = useState('');
  const [isFinished, setIsFinished] = useState(false);
  const [hasResume, setHasResume] = useState(null); // null = checking, true/false = result
  const [availableDomains, setAvailableDomains] = useState([]);

  const navigate = useNavigate();
  const speakTimeoutRef = useRef(null);
  const isMountedRef = useRef(true);
  const [questionNumber, setQuestionNumber] = useState(1);

  // Helper for voice
  const speak = (text) => {
    if (!window.speechSynthesis) return;

    if (speakTimeoutRef.current) {
      clearTimeout(speakTimeoutRef.current);
    }

    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
      window.speechSynthesis.cancel();
      if (window.speechSynthesis.paused) window.speechSynthesis.resume();
    }

    speakTimeoutRef.current = setTimeout(() => {
      if (!isMountedRef.current) return;

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    }, 150);
  };

  // CLEANUP: Stop speaking when leaving page
  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
      if (speakTimeoutRef.current) {
        clearTimeout(speakTimeoutRef.current);
      }
      if (window.speechSynthesis) {
        window.speechSynthesis.pause();
        window.speechSynthesis.cancel();
        if (window.speechSynthesis.paused) {
          window.speechSynthesis.resume();
        }
      }
    };
  }, []);

  // Check if user has uploaded resume on component mount
  useEffect(() => {
    const checkResume = async () => {
      try {
        const data = await getInterviewDomains();
        if (data.domains && data.domains.length > 0) {
          setHasResume(true);
          setAvailableDomains(data.domains);
        } else {
          setHasResume(false);
        }
      } catch (err) {
        console.error("Failed to check resume:", err);
        setHasResume(false);
      }
    };
    checkResume();
  }, []);

  // Categories supported by backend (from debug script/code)
  const categories = [
    { id: 'python', label: 'Python Developer' },
    { id: 'backend', label: 'Backend Engineering' },
    { id: 'hr', label: 'HR / Behavioral' }
  ];

  const handleStartInterview = async (domain) => {
    setLoading(true);
    setError(null);
    try {
      const data = await startInterview(domain);
      // data format based on backend: { session_id, question_number, question }
      setSessionId(data.session_id);
      setQuestionNumber(data.question_number || 1);
      const newQ = {
        question: data.question,
        tips: "Answer based on your experience. The AI will evaluate your response."
      };
      setCurrentQuestion(newQ);
      speak(newQ.question); // Voice support
      setIsFinished(false);
      setUserAnswer('');
      setShowFeedback(false);
      setScore(null);
    } catch (err) {
      console.error("Start interview failed:", err);
      if (err.detail && err.detail.includes("Resume not uploaded")) {
        // Redirect to resume upload or show specific message
        setError(
          <span>
            Resume not uploaded. <button onClick={() => navigate('/resume-upload')} className="underline font-bold">Upload Resume</button> to start.
          </span>
        );
      } else {
        setError(err.detail || "Failed to start interview. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!userAnswer.trim()) return;

    setLoading(true);
    try {
      const data = await apiSubmitAnswer(sessionId, userAnswer);
      // data format: { interview_finished, final_score_percentage, message, question... }

      if (data.interview_finished) {
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        setIsFinished(true);
        setFeedbackMsg(data.message);
        setScore(data.final_score_percentage); // Final score
        setShowFeedback(true);
      } else {
        // Next question
        setQuestionNumber(data.question_number || (questionNumber + 1));
        const nextQ = {
          question: data.question,
          tips: "Keep going! Good luck."
        };
        setCurrentQuestion(nextQ);
        speak(nextQ.question); // Voice support
        setUserAnswer('');
        setShowFeedback(false);
      }
    } catch (err) {
      console.error("Submit answer failed:", err);
      setError("Failed to submit answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6"> Interview Preparation</h1>

      {error && (
        <div className="mb-6 p-4 bg-red-100 text-red-700 rounded-lg border border-red-200">
          {error}
        </div>
      )}

      {/* Resume Upload Prompt - Shows when no resume detected */}
      {hasResume === false && (
        <div className="mb-6 p-6 bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-300 rounded-lg shadow-md">
          <div className="flex items-start gap-4">
            <div className="text-4xl"></div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-yellow-900 mb-2">
                Resume Required for Personalized Interview
              </h3>
              <p className="text-yellow-800 mb-4">
                To get interview questions tailored to your skills and experience, please upload your resume first.
                We'll analyze it and create a personalized interview session based on your background.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => navigate('/resume-upload')}
                  className="bg-yellow-600 text-white px-6 py-3 rounded-lg hover:bg-yellow-700 font-medium shadow-sm transition-colors"
                >
                  Upload Resume Now
                </button>
                <button
                  onClick={() => setHasResume(null)}
                  className="bg-white text-yellow-700 px-6 py-3 rounded-lg hover:bg-yellow-50 font-medium border border-yellow-300 transition-colors"
                >
                  I Already Uploaded
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Loading state while checking resume */}
      {hasResume === null && (
        <div className="mb-6 p-4 bg-blue-50 text-blue-700 rounded-lg border border-blue-200">
          <p>Checking your resume status...</p>
        </div>
      )}

      {!sessionId || isFinished ? (
        <div>
          {/* Category Selection */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Choose Interview Domain</h2>
            <div className="flex gap-4 mb-6 flex-wrap">
              {categories.map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategory(cat.id)}
                  className={`px-4 py-2 rounded-lg ${selectedCategory === cat.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>

            <div className="mt-6">
              <button
                onClick={() => handleStartInterview(selectedCategory)}
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 text-lg font-medium"
              >
                {loading ? "Starting..." : "Start Practice Interview"}
              </button>
              <p className="mt-2 text-sm text-gray-500">
                This will generate a personalized interview session based on your uploaded resume.
              </p>
            </div>
          </div>

          {isFinished && score !== null && (
            <div className="p-6 bg-green-50 border border-green-200 rounded-lg mb-8">
              <h3 className="text-2xl font-bold text-green-800 mb-2">Interview Completed!</h3>
              <p className="text-lg">Your Final Score: <span className="font-bold">{score}%</span></p>
              <p className="text-gray-700 mt-2">{feedbackMsg}</p>
              <button
                onClick={() => {
                  if (window.speechSynthesis) {
                    window.speechSynthesis.pause();
                    window.speechSynthesis.cancel();
                    if (window.speechSynthesis.paused) window.speechSynthesis.resume();
                  }
                  setSessionId(null);
                  setIsFinished(false);
                }}
                className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Start New Session
              </button>
            </div>
          )}
        </div>
      ) : (
        <div>
          {/* Practice Session */}
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">
                Practice Session - Question {questionNumber}
              </h2>
              <button
                onClick={() => {
                  if (window.speechSynthesis) {
                    window.speechSynthesis.pause();
                    window.speechSynthesis.cancel();
                    if (window.speechSynthesis.paused) window.speechSynthesis.resume();
                  }
                  setSessionId(null);
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                Exit Session
              </button>
            </div>

            <div className="mb-4">
              <h3 className="text-lg font-medium mb-2">{currentQuestion?.question}</h3>
              <p className="text-gray-600 text-sm mb-4">💡 {currentQuestion?.tips}</p>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Your Answer:</label>
              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Type your answer here..."
                className="w-full p-3 border rounded-lg h-32 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
            </div>

            <button
              onClick={handleSubmitAnswer}
              disabled={!userAnswer.trim() || loading}
              className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
            >
              {loading ? "Submitting..." : "Submit Answer"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default InterviewPrep;
