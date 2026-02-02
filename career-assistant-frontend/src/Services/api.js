import axios from "axios";

/* =========================
   AXIOS INSTANCE
========================= */

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
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
    query,          // ✅ backend expects "query"
    role: "user",   // ✅ FIX for 422 (missing role)
  });
  return res.data;
};

/* =========================
   RESUME APIs (FIXED ✅)
========================= */

/**
 * Upload & analyze resume
 * Backend expects: file: UploadFile = File(...)
 */
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file); // ✅ MUST be "file"

  const res = await api.post("/resume/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};

/* =========================
   CHATBOT APIs (FIXED ✅)
========================= */

/**
 * Create new chatbot session
 * POST /chatbot/session/new
 */
export const createChatSession = async () => {
  const res = await api.post("/chatbot/session/new");
  return res.data; // { session_id }
};

/**
 * Send message to chatbot
 * POST /chatbot/session/{session_id}/query
 */
export const sendChatbotMessage = async (query, sessionId) => {
  const res = await api.post(
    `/chatbot/session/${sessionId}/query`,
    {
      query,
      role: "user", // ✅ REQUIRED by backend schema
    }
  );
  return res.data; // { reply }
};

/* =========================
   INTERVIEW APIs
========================= */

export const startInterview = async (data) => {
  const res = await api.post("/interview/start", data);
  return res.data;
};

/* =========================
   UTILS
========================= */

export const pingBackend = async () => {
  const res = await api.get("/ping");
  return res.data;
};
