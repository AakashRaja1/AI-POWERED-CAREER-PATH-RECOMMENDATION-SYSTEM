import React, { useState, useRef, useEffect } from "react";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { 
      sender: "bot", 
      text: "Hello! I'm your AI Career Assistant 🤖. I'm here to help you with career guidance, skill development, and job market insights. How can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { 
      sender: "user", 
      text: input,
      timestamp: new Date()
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chatbot/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          user_id: "user_" + Date.now(),
          message: input 
        })
      });

      const data = await res.json();

      const botMessage = { 
        sender: "bot", 
        text: data.reply,
        timestamp: new Date()
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const botMessage = {
        sender: "bot",
        text: "Oops! I'm having trouble connecting right now. Please try again in a moment. 🔌",
        timestamp: new Date()
      };
      setMessages((prev) => [...prev, botMessage]);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    "What career suits me best?",
    "How to improve my skills?",
    "Latest job market trends",
    "Career switch advice"
  ];

  const handleQuickQuestion = (question) => {
    setInput(question);
  };

  return (
    <div className="relative min-h-screen bg-linear-to-br from-blue-50 via-purple-50 to-pink-50 overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 -left-20 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 -right-20 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-pink-400/10 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="relative z-10 flex flex-col h-screen px-4 py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-6 animate-fadeIn">
          <div className="inline-flex items-center gap-3 bg-white/80 backdrop-blur-md rounded-2xl px-6 py-4 shadow-lg border border-gray-200 mb-4">
            <div className="w-12 h-12 bg-linear-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-2xl shadow-lg">
              🤖
            </div>
            <div className="text-left">
              <h1 className="text-2xl sm:text-3xl font-extrabold bg-linear-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                AI Career Assistant
              </h1>
              <p className="text-sm text-gray-600">Always here to help you succeed</p>
            </div>
          </div>
        </div>

        {/* Chat Container */}
        <div className="flex-1 max-w-5xl w-full mx-auto mb-6 overflow-hidden">
          <div 
            ref={chatContainerRef}
            className="h-full overflow-y-auto px-4 py-6 space-y-4 bg-white/40 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent"
          >
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} animate-slideUp`}
              >
                <div className={`flex gap-3 max-w-[85%] sm:max-w-[70%] ${msg.sender === "user" ? "flex-row-reverse" : "flex-row"}`}>
                  {/* Avatar */}
                  <div className={`shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-xl shadow-lg ${
                    msg.sender === "user" 
                      ? "bg-linear-to-r from-blue-600 to-purple-600" 
                      : "bg-linear-to-r from-purple-500 to-pink-500"
                  }`}>
                    {msg.sender === "user" ? "👤" : "🤖"}
                  </div>
                  
                  {/* Message Bubble */}
                  <div className="flex flex-col">
                    <div
                      className={`px-5 py-3 rounded-2xl shadow-md ${
                        msg.sender === "user"
                          ? "bg-linear-to-r from-blue-600 to-purple-600 text-white rounded-tr-none"
                          : "bg-white text-gray-800 rounded-tl-none border border-gray-100"
                      }`}
                    >
                      <p className="text-sm sm:text-base leading-relaxed whitespace-pre-wrap wrap-break-word">
                        {msg.text}
                      </p>
                    </div>
                    <span className={`text-xs text-gray-500 mt-1 px-2 ${msg.sender === "user" ? "text-right" : "text-left"}`}>
                      {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start animate-slideUp">
                <div className="flex gap-3 max-w-[70%]">
                  <div className="shrink-0 w-10 h-10 rounded-full bg-linear-to-r from-purple-500 to-pink-500 flex items-center justify-center text-xl shadow-lg">
                    🤖
                  </div>
                  <div className="bg-white text-gray-800 px-5 py-3 rounded-2xl rounded-tl-none shadow-md border border-gray-100">
                    <div className="flex gap-2 items-center">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Quick Questions - Show only if no messages from user yet */}
        {messages.length === 1 && (
          <div className="max-w-5xl w-full mx-auto mb-4 animate-fadeIn">
            <p className="text-sm text-gray-600 mb-3 px-4">💡 Quick questions to get started:</p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 px-4">
              {quickQuestions.map((question, idx) => (
                <button
                  key={idx}
                  onClick={() => handleQuickQuestion(question)}
                  className="bg-white/80 backdrop-blur-sm hover:bg-white border border-gray-200 hover:border-blue-400 text-gray-700 hover:text-blue-600 px-4 py-2 rounded-xl text-xs sm:text-sm transition-all duration-300 transform hover:scale-105 hover:shadow-md"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="max-w-5xl w-full mx-auto">
          <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl border border-gray-200 p-4">
            <div className="flex gap-3 items-end">
              <div className="flex-1">
                <textarea
                  rows="1"
                  className="w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-all duration-300"
                  placeholder="Type your message here... (Press Enter to send)"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  style={{ minHeight: '48px', maxHeight: '120px' }}
                />
              </div>
              <button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className={`bg-linear-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold px-6 py-3 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center gap-2 ${
                  (!input.trim() || loading) ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                <span className="text-xl">
                  {loading ? "⏳" : "📤"}
                </span>
                <span className="hidden sm:inline">Send</span>
              </button>
            </div>
            
            {/* Tips */}
            <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
              <span>💡 Tip:</span>
              <span>Ask about career paths, skills, certifications, or job market trends</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
