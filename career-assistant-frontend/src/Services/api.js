import axios from "axios";

/* =========================
   AXIOS INSTANCE
========================= */

// Determine API base URL
const isLocalhost = typeof window !== "undefined" && /localhost|127\.0\.0\.1|\[::1\]/.test(window.location.hostname);
const envApi = process.env.REACT_APP_API_URL && process.env.REACT_APP_API_URL.trim();
const fallbackProd = typeof window !== "undefined" ? window.location.origin : "";
const baseURL = isLocalhost ? (envApi || "http://localhost:8000") : (envApi || fallbackProd);

const api = axios.create({
  baseURL: baseURL,
});

/* =========================
   AUTH INTERCEPTOR
========================= */

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle 401/403 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      console.log("Auth error detected, clearing token.");
      localStorage.removeItem("authToken");
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;

/* =========================
   AUTH APIs
========================= */

export const loginUser = async (formData) => {
  const res = await api.post("/auth/login", formData);
  return res.data;
};

export const registerUser = async (formData) => {
  const res = await api.post("/auth/register", formData);
  return res.data;
};

/* =========================
   JOB APIs
========================= */

export const getAvailableJobs = async () => {
  const res = await api.get("/jobs/available");
  return res.data;
};

export const searchJobs = async (query) => {
  const res = await api.post("/jobs/search", {
    query,
    role: "user",
  });
  return res.data;
};

/* =========================
   RESUME APIs
========================= */

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await api.post("/resume/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  } catch (err) {
    throw err.response?.data || "Resume upload failed";
  }
};

/* =========================
   CHATBOT APIs
========================= */

export const createChatSession = async () => {
  const res = await api.post("/chatbot/session/new");
  return res.data;
};

export const sendChatbotMessage = async (query, sessionId) => {
  const res = await api.post(
    `/chatbot/session/${sessionId}/query`,
    {
      query,
      role: "user",
    }
  );
  return res.data;
};

/* =========================
   INTERVIEW APIs
========================= */

export const startInterview = async (domain) => {
  try {
    const res = await api.post("/interview/start", { domain });
    return res.data;
  } catch (err) {
    throw err.response?.data || "Failed to start interview";
  }
};

export const submitAnswer = async (sessionId, answer) => {
  try {
    const res = await api.post("/interview/answer", {
      session_id: sessionId,
      answer: answer
    });
    return res.data;
  } catch (err) {
    throw err.response?.data || "Failed to submit answer";
  }
};

export const getInterviewDomains = async () => {
  try {
    const res = await api.get("/interview/domains");
    return res.data;
  } catch (err) {
    throw err.response?.data || "Failed to fetch domains";
  }
};

/* =========================
   CHEATING DETECTION
========================= */

export const recordTabSwitch = async (sessionId) => {
  const res = await api.post("/cheating/tab-switch", { session_id: sessionId });
  return res.data;
};

export const analyzeInterviewFrame = async (sessionId, frameBase64) => {
  const res = await api.post("/cheating/frame", {
    session_id: sessionId,
    frame: frameBase64
  });
  return res.data;
};

/* =========================
   UTILS
========================= */

export const pingBackend = async () => {
  const res = await api.get("/ping");
  return res.data;
};
