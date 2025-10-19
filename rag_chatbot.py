"""
RAG-based Chatbot with Memory for Career Assistant
Implements Retrieval-Augmented Generation with conversation memory
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any
from career_knowledge_base import search_knowledge, get_knowledge_by_category

class ChatMemory:
    """Manages conversation memory and context"""
    
    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.conversations = {}  # session_id -> conversation history
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Dict = None):
        """Add a message to conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        message = {
            "id": str(uuid.uuid4()),
            "role": role,  # 'user' or 'assistant'
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversations[session_id].append(message)
        
        # Keep only recent messages
        if len(self.conversations[session_id]) > self.max_messages:
            self.conversations[session_id] = self.conversations[session_id][-self.max_messages:]
    
    def get_conversation_context(self, session_id: str, max_messages: int = 5) -> List[Dict]:
        """Get recent conversation context"""
        if session_id not in self.conversations:
            return []
        
        return self.conversations[session_id][-max_messages:]
    
    def get_user_preferences(self, session_id: str) -> Dict:
        """Extract user preferences from conversation history"""
        if session_id not in self.conversations:
            return {}
        
        preferences = {
            "interests": [],
            "experience_level": None,
            "industry": None,
            "location": None
        }
        
        # Analyze conversation for preferences
        for message in self.conversations[session_id]:
            if message["role"] == "user":
                content = message["content"].lower()
                
                # Extract experience level
                if any(word in content for word in ["intern", "internship", "entry level", "beginner"]):
                    preferences["experience_level"] = "entry"
                elif any(word in content for word in ["senior", "experienced", "5 years", "lead"]):
                    preferences["experience_level"] = "senior"
                elif any(word in content for word in ["junior", "2 years", "3 years"]):
                    preferences["experience_level"] = "mid"
                
                # Extract industry interests
                industries = ["tech", "technology", "software", "finance", "healthcare", "marketing", "sales"]
                for industry in industries:
                    if industry in content:
                        preferences["interests"].append(industry)
                
                # Extract location
                if "remote" in content:
                    preferences["location"] = "remote"
                elif any(city in content for city in ["bangalore", "mumbai", "delhi", "hyderabad", "chennai"]):
                    preferences["location"] = "india"
        
        return preferences

class RAGChatbot:
    """RAG-based chatbot with memory and context awareness"""
    
    def __init__(self):
        self.memory = ChatMemory()
        self.system_prompt = """You are a helpful career assistant AI. You provide personalized career advice based on the user's context and conversation history. 
        
        Guidelines:
        - Be encouraging and supportive
        - Provide specific, actionable advice
        - Reference relevant information from the knowledge base
        - Consider the user's experience level and interests
        - Maintain conversation context
        - Ask follow-up questions when appropriate
        """
    
    def retrieve_relevant_knowledge(self, query: str, user_preferences: Dict) -> List[Dict]:
        """Retrieve relevant knowledge based on query and user context"""
        # Search knowledge base
        knowledge_results = search_knowledge(query)
        
        # Filter by user preferences if available
        if user_preferences.get("experience_level"):
            # Could add experience-specific filtering here
            pass
        
        # Return top 3 most relevant results
        return knowledge_results[:3]
    
    def generate_response(self, query: str, session_id: str) -> Dict:
        """Generate response using RAG pipeline"""
        
        # Get conversation context
        context = self.memory.get_conversation_context(session_id)
        
        # Get user preferences
        user_preferences = self.memory.get_user_preferences(session_id)
        
        # Retrieve relevant knowledge
        relevant_knowledge = self.retrieve_relevant_knowledge(query, user_preferences)
        
        # Add user message to memory
        self.memory.add_message(session_id, "user", query)
        
        # Generate response (in a real implementation, this would use an LLM)
        response = self._generate_llm_response(query, context, relevant_knowledge, user_preferences)
        
        # Add assistant response to memory
        self.memory.add_message(session_id, "assistant", response["message"], {
            "knowledge_used": [k["id"] for k in relevant_knowledge],
            "user_preferences": user_preferences
        })
        
        return response
    
    def _generate_llm_response(self, query: str, context: List[Dict], knowledge: List[Dict], preferences: Dict) -> Dict:
        """Generate response using retrieved knowledge and context"""
        
        # Build context-aware response
        response_parts = []
        suggestions = []
        
        # Use retrieved knowledge to inform response
        if knowledge:
            # Primary response based on knowledge
            main_knowledge = knowledge[0]
            response_parts.append(main_knowledge["content"])
            
            # Add additional insights from other knowledge
            for k in knowledge[1:]:
                if k["category"] != main_knowledge["category"]:
                    response_parts.append(f"Additionally, {k['content']}")
        
        # Add personalized suggestions based on preferences
        if preferences.get("experience_level") == "entry":
            suggestions.extend([
                "Consider applying for internships to gain experience",
                "Build a strong portfolio with personal projects",
                "Network with professionals in your field"
            ])
        elif preferences.get("experience_level") == "senior":
            suggestions.extend([
                "Highlight your leadership experience",
                "Consider mentoring junior professionals",
                "Focus on strategic impact in your applications"
            ])
        
        # Add context-aware suggestions
        if "interview" in query.lower():
            suggestions.extend([
                "Practice with mock interviews",
                "Prepare specific examples using the STAR method",
                "Research the company thoroughly"
            ])
        elif "resume" in query.lower():
            suggestions.extend([
                "Tailor your resume for each application",
                "Use action verbs and quantify achievements",
                "Keep it to 1-2 pages maximum"
            ])
        elif "salary" in query.lower():
            suggestions.extend([
                "Research market rates for your role",
                "Consider total compensation package",
                "Practice your negotiation pitch"
            ])
        
        # Combine response
        if not response_parts:
            response_parts.append("I'd be happy to help you with your career questions! Could you tell me more about what specific area you'd like advice on?")
        
        response_message = " ".join(response_parts)
        
        return {
            "message": response_message,
            "suggestions": suggestions[:4],  # Limit to 4 suggestions
            "knowledge_sources": [k["id"] for k in knowledge],
            "context_used": len(context),
            "personalized": bool(preferences)
        }
    
    def get_conversation_summary(self, session_id: str) -> Dict:
        """Get summary of conversation for user"""
        context = self.memory.get_conversation_context(session_id)
        preferences = self.memory.get_user_preferences(session_id)
        
        return {
            "message_count": len(context),
            "user_preferences": preferences,
            "recent_topics": [msg["content"][:50] + "..." for msg in context[-3:] if msg["role"] == "user"]
        }

# Global chatbot instance
rag_chatbot = RAGChatbot()
