import React, { useState, useEffect } from 'react';

const InterviewSession = () => {
    const [sessionId, setSessionId] = useState(null);
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [finished, setFinished] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    // Start interview on mount
    useEffect(() => {
        startInterview();
    }, []);

    const startInterview = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await fetch('http://localhost:8000/interview/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ domain: 'python' }) // Default domain
            });

            if (!response.ok) throw new Error('Failed to start interview');

            const data = await response.json();
            setSessionId(data.session_id);
            setCurrentQuestion(data.question);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const submitAnswer = async (e) => {
        e.preventDefault();
        if (!answer.trim()) return;

        setLoading(true);
        setError('');
        try {
            const response = await fetch('http://localhost:8000/interview/answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    answer: answer
                })
            });

            if (!response.ok) throw new Error('Failed to submit answer');

            const data = await response.json();

            if (data.interview_finished) {
                setFinished(true);
                setResult(data);
            } else {
                setCurrentQuestion(data.question);
                setAnswer('');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading && !currentQuestion && !finished) return <div>Loading interview...</div>;
    if (error) return <div className="text-red-500">Error: {error}</div>;

    if (finished) {
        return (
            <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4">
                <h2 className="text-2xl font-bold text-green-600">Interview Completed!</h2>
                <p>{result.message}</p>
                <div className="text-xl">
                    Final Score: <span className="font-bold">{result.final_score_percentage}%</span>
                </div>
                <button
                    onClick={() => window.location.reload()}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                    Start New Interview
                </button>
            </div>
        );
    }

    return (
        <div className="p-6 max-w-2xl mx-auto bg-white rounded-xl shadow-md space-y-6">
            <div className="flex justify-between items-center border-b pb-4">
                <h2 className="text-xl font-bold text-gray-800">Mock Interview</h2>
                <span className="text-sm text-gray-500">Session ID: {sessionId?.slice(0, 8)}...</span>
            </div>

            <div className="space-y-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-blue-800 mb-2">Current Question:</h3>
                    <p className="text-lg text-gray-800">{currentQuestion}</p>
                </div>

                <form onSubmit={submitAnswer} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Your Answer:
                        </label>
                        <textarea
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="Type your answer here..."
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full py-3 px-4 rounded-lg text-white font-medium ${loading
                                ? 'bg-gray-400 cursor-not-allowed'
                                : 'bg-indigo-600 hover:bg-indigo-700'
                            }`}
                    >
                        {loading ? 'Submitting...' : 'Submit Answer'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default InterviewSession;
