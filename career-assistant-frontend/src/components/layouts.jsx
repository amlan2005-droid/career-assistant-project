import { Link } from "react-router-dom";
import { Briefcase, LayoutDashboard, MessageCircle, FileText, LogOut } from "lucide-react"; 

export default function Layout({ children }) {
  // Temporarily disable authentication for development
  const logout = () => {
    console.log('Logout clicked - authentication disabled for development');
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-lg flex flex-col">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-blue-600">Career Assist</h1>
        </div>
        <nav className="flex-1 p-4 space-y-3">
          <Link to="/dashboard" className="flex items-center gap-2 p-2 rounded-lg hover:bg-blue-100">
            <LayoutDashboard size={20} /> Dashboard
          </Link>
          <Link to="/jobs" className="flex items-center gap-2 p-2 rounded-lg hover:bg-blue-100">
            <Briefcase size={20} /> Jobs
          </Link>
          <Link to="/interview-prep" className="flex items-center gap-2 p-2 rounded-lg hover:bg-blue-100">
            <FileText size={20} /> Interview Prep
          </Link>
          <Link to="/chatbot" className="flex items-center gap-2 p-2 rounded-lg hover:bg-blue-100">
            <MessageCircle size={20} /> Chatbot
          </Link>
        </nav>
        <div className="p-4 border-t">
          <button
            onClick={logout}
            className="flex items-center gap-2 w-full p-2 rounded-lg text-red-600 hover:bg-red-100"
          >
            <LogOut size={20} /> Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
