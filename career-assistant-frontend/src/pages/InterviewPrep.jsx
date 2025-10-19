// src/pages/InterviewPrep.jsx
import React, { useState } from 'react';
import FeedbackCard from '../components/FeedbackCard';

const InterviewPrep = () => {
  const [selectedCategory, setSelectedCategory] = useState('general');
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);

  const interviewQuestions = {
    general: [
      {
        id: 1,
        question: "Tell me about yourself.",
        tips: "Structure your answer: education, relevant experience, key skills, and career goals.",
        sampleAnswer: "I am a computer science student with a passion for software development. I have experience in React and Python, and I'm particularly interested in full-stack development."
      },
      {
        id: 2,
        question: "Why do you want to work for our company?",
        tips: "Research the company, mention specific values or products that align with your interests.",
        sampleAnswer: "I'm excited about your company's innovative approach to technology and your commitment to user experience."
      },
      {
        id: 3,
        question: "What are your strengths and weaknesses?",
        tips: "Be honest about weaknesses but show how you're working to improve them.",
        sampleAnswer: "My strength is problem-solving. My weakness is public speaking, but I'm taking courses to improve."
      }
    ],
    technical: [
      {
        id: 4,
        question: "What is a REST API?",
        tips: "Explain the concept, mention HTTP methods, and give a real-world example.",
        sampleAnswer: "REST API is a way for applications to communicate over HTTP. It uses methods like GET, POST, PUT, DELETE to perform operations on resources."
      },
      {
        id: 5,
        question: "Explain the difference between SQL and NoSQL databases.",
        tips: "Compare structure, scalability, and use cases for each type.",
        sampleAnswer: "SQL databases are relational with structured data, while NoSQL databases are non-relational and more flexible for unstructured data."
      },
      {
        id: 6,
        question: "What is version control and why is it important?",
        tips: "Explain Git concepts, branching, and collaboration benefits.",
        sampleAnswer: "Version control tracks changes in code over time, allowing teams to collaborate, revert changes, and maintain code history."
      }
    ],
    behavioral: [
      {
        id: 7,
        question: "Tell me about a time you faced a difficult challenge.",
        tips: "Use the STAR method: Situation, Task, Action, Result.",
        sampleAnswer: "In my last project, I had to learn a new framework in a week. I broke it down into daily goals and successfully delivered the project."
      },
      {
        id: 8,
        question: "How do you handle working under pressure?",
        tips: "Give a specific example and explain your stress management techniques.",
        sampleAnswer: "I prioritize tasks, break them into smaller chunks, and communicate with my team about deadlines and challenges."
      }
    ]
  };

  const startPractice = (question) => {
    setCurrentQuestion(question);
    setUserAnswer('');
    setShowFeedback(false);
  };

  const submitAnswer = () => {
    if (userAnswer.trim()) {
      setShowFeedback(true);
    }
  };

  const getFeedback = (question, answer) => {
    // Simple feedback logic - in a real app, this would use AI
    const feedback = {
      score: Math.floor(Math.random() * 3) + 7, // Random score 7-9
      feedback: `Good answer! You covered the main points. ${question.tips}`
    };
    return feedback;
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">🎯 Interview Preparation</h1>
      
      {!currentQuestion ? (
        <div>
          {/* Category Selection */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Choose Interview Category</h2>
            <div className="flex gap-4 mb-6">
              <button
                onClick={() => setSelectedCategory('general')}
                className={`px-4 py-2 rounded-lg ${
                  selectedCategory === 'general' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                General Questions
              </button>
              <button
                onClick={() => setSelectedCategory('technical')}
                className={`px-4 py-2 rounded-lg ${
                  selectedCategory === 'technical' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Technical Questions
              </button>
              <button
                onClick={() => setSelectedCategory('behavioral')}
                className={`px-4 py-2 rounded-lg ${
                  selectedCategory === 'behavioral' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Behavioral Questions
              </button>
            </div>
          </div>

          {/* Questions List */}
          <div className="grid gap-4">
            {interviewQuestions[selectedCategory].map((q) => (
              <div key={q.id} className="bg-white p-6 rounded-lg shadow border">
                <h3 className="text-lg font-semibold mb-2">{q.question}</h3>
                <p className="text-gray-600 mb-3">{q.tips}</p>
                <button
                  onClick={() => startPractice(q)}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Practice This Question
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div>
          {/* Practice Session */}
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Practice Session</h2>
              <button
                onClick={() => setCurrentQuestion(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ← Back to Questions
              </button>
            </div>
            
            <div className="mb-4">
              <h3 className="text-lg font-medium mb-2">{currentQuestion.question}</h3>
              <p className="text-gray-600 text-sm mb-4">💡 {currentQuestion.tips}</p>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Your Answer:</label>
              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Type your answer here..."
                className="w-full p-3 border rounded-lg h-32 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={showFeedback}
              />
            </div>

            {!showFeedback ? (
              <button
                onClick={submitAnswer}
                disabled={!userAnswer.trim()}
                className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
              >
                Submit Answer
              </button>
            ) : (
              <div className="mt-4">
                <FeedbackCard
                  question={currentQuestion.question}
                  answer={userAnswer}
                  feedback={getFeedback(currentQuestion, userAnswer).feedback}
                  score={getFeedback(currentQuestion, userAnswer).score}
                />
                <div className="mt-4 flex gap-4">
                  <button
                    onClick={() => {
                      setUserAnswer('');
                      setShowFeedback(false);
                    }}
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                  >
                    Try Again
                  </button>
                  <button
                    onClick={() => setCurrentQuestion(null)}
                    className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                  >
                    Next Question
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Previous Feedback */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Recent Practice Sessions</h2>
        <div className="space-y-4">
          <FeedbackCard
            question="Tell me about yourself."
            answer="I am a 2nd-year CS student passionate about software development..."
            feedback="You spoke clearly and confidently. Try to structure your answer with education, projects, and goals."
            score={8}
          />
          <FeedbackCard
            question="What is a REST API?"
            answer="It allows communication between client and server using HTTP methods."
            feedback="Good definition! You can improve it by mentioning statelessness and resource-based architecture."
            score={9}
          />
        </div>
      </div>
    </div>
  );
};

export default InterviewPrep;
