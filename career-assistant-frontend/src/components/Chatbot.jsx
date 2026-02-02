import React, { useState, useEffect, useRef } from "react";

const COOLDOWN_SECONDS = 8;

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hi! How can I help you today?", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [cooldown, setCooldown] = useState(0);
  const messagesEndRef = useRef(null);

  /* -------------------- Auto scroll -------------------- */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  /* -------------------- Cooldown timer -------------------- */
  useEffect(() => {
    if (cooldown <= 0) return;

    const timer = setInterval(() => {
      setCooldown(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [cooldown]);

  /* -------------------- Create session -------------------- */
  const createSession = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/chatbot/session/new", {
        method: "POST"
      });

      const data = await res.json();
      setSessionId(data.session_id);
      return data.session_id;
    } catch {
      setMessages(prev => [
        ...prev,
        { text: "Unable to create session.", sender: "bot" }
      ]);
      return null;
    }
  };

  useEffect(() => {
    createSession();
  }, []);

  /* -------------------- SEND MESSAGE -------------------- */
  const handleSend = async () => {
    if (!input.trim() || isLoading || cooldown > 0) return;

    const text = input;
    setInput("");
    setIsLoading(true);

    setMessages(prev => [...prev, { text, sender: "user" }]);

    try {
      const sid = sessionId || await createSession();
      if (!sid) return;

      const res = await fetch(
        `http://127.0.0.1:8000/chatbot/session/${sid}/query`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: text })
        }
      );

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { text: data.reply || "No response from AI.", sender: "bot" }
      ]);

      setCooldown(COOLDOWN_SECONDS);
    } catch {
      setMessages(prev => [
        ...prev,
        { text: "Server unreachable.", sender: "bot" }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  /* -------------------- UI -------------------- */
  return (
    <div className="flex flex-col h-[500px] max-w-lg mx-auto border rounded-lg">
      <div className="bg-blue-600 text-white p-4 font-bold">
        Career Assistant AI
      </div>

      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`p-3 rounded-lg max-w-[80%] ${m.sender === "user" ? "bg-blue-500 text-white" : "bg-white border"}`}>
              {m.text}
            </div>
          </div>
        ))}
        {isLoading && <p className="italic text-gray-400">AI is typing…</p>}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-3 border-t flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
          disabled={isLoading || cooldown > 0}
          placeholder={cooldown > 0 ? `Wait ${cooldown}s...` : "Type a message"}
        />

        <button
          onClick={handleSend}
          disabled={isLoading || cooldown > 0 || !input.trim()}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:bg-gray-300"
        >
          {cooldown > 0 ? `${cooldown}s` : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
