// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Home from './pages/Home';
import Jobs from './pages/job';
import InterviewPrep from './pages/InterviewPrep';
import OnboardingForm from './components/OnboardingForm';
import Chatbot from './pages/Chatbot';

import Login from './pages/login';
import Register from './pages/Register';
import ResumeUpload from './pages/ResumeUpload';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/jobs" element={<Jobs />} />
            <Route path="/interview-prep" element={<InterviewPrep />} />
            <Route path="/onboarding" element={<OnboardingForm />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/resume-upload" element={<ResumeUpload />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;