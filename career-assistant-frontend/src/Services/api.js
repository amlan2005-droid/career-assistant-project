import axios from "axios";

// Determine API base URL
const isLocalhost = typeof window !== "undefined" && /localhost|127\.0\.0\.1|\[::1\]/.test(window.location.hostname);
const envApi = process.env.REACT_APP_API_URL && process.env.REACT_APP_API_URL.trim();
const fallbackProd = typeof window !== "undefined" ? window.location.origin : "";
const baseURL = isLocalhost ? (envApi || "http://localhost:3000") : (envApi || fallbackProd);

const API = axios.create({
  baseURL,
});

// Request interceptor for API calls
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers["Authorization"] = "Bearer " + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- LOGIN ---
export const loginUser = async (formData) => {
  try {
    const res = await API.post("/auth/login", formData);
    return res.data;
  } catch (err) {
    throw err.response?.data || "Login failed";
  }
};

// --- REGISTER ---
export const registerUser = async (formData) => {
  try {
    const res = await API.post("/auth/register", formData);
    return res.data;
  } catch (err) {
    throw err.response?.data || "Registration failed";
  }
};

// --- JOBS: Get available jobs ---
export const getAvailableJobs = async () => {
  try {
    const res = await API.get("/jobs/available");
    return res.data;
  } catch (err) {
    throw err.response?.data || "Failed to fetch jobs";
  }
};

// --- JOBS: Search jobs (POST JSON payload) ---
export const searchJobs = async (query) => {
  try {
    const res = await API.post("/jobs/search", { query });
    return res.data;
  } catch (err) {
    throw err.response?.data || "Job search failed";
  }
};

// --- PING BACKEND ---
export const pingBackend = async () => {
  try {
    const res = await API.get("/ping");
    return res.data;
  } catch (err) {
    throw err.response?.data || "Backend not reachable";
  }
};

// --- RESUME: Upload resume file ---
export const uploadResume = async (formData) => {
  try {
    const res = await API.post("/resume/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  } catch (err) {
    throw err.response?.data || "Resume upload failed";
  }
};

// --- CHATBOT: Create new session ---
export const createChatSession = async () => {
  try {
    const res = await API.post("/chatbot/session/new");
    return res.data;
  } catch (err) {
    throw err.response?.data || "Failed to create chat session";
  }
};

// --- CHATBOT: Send message with session ---
export const sendChatbotMessage = async (message, sessionId = null) => {
  try {
    const payload = { message };
    if (sessionId) payload.session_id = sessionId;
    const res = await API.post("/chatbot/message", payload);
    return res.data;
  } catch (err) {
    throw err.response?.data || "Chatbot request failed";
  }
};

// --- CHATBOT: Get session summary ---
export const getChatSessionSummary = async (sessionId) => {
  try {
    const res = await API.get(`/chatbot/session/${sessionId}/summary`);
    return res.data;
  } catch (err) {
    throw err.response?.data || "Failed to get session summary";
  }
};
