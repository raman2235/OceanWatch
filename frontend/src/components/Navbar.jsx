import { Link } from "react-router-dom";
import { useState } from "react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="text-blue-900 font-bold text-xl">
          🌊 OceanHazard
        </Link>

        {/* Desktop Links */}
        <div className="hidden md:flex space-x-6">
          <Link to="/" className="text-gray-700 hover:text-blue-600">Home</Link>
          <Link to="/dashboard" className="text-gray-700 hover:text-blue-600">Dashboard</Link>
          <Link to="/report" className="text-gray-700 hover:text-blue-600">Report</Link>
          <Link to="/login" className="text-gray-700 hover:text-blue-600">Login</Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden text-gray-700"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? "✖" : "☰"}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-white px-6 py-4 space-y-2 shadow-md">
          <Link to="/" className="block text-gray-700 hover:text-blue-600">Home</Link>
          <Link to="/dashboard" className="block text-gray-700 hover:text-blue-600">Dashboard</Link>
          <Link to="/report" className="block text-gray-700 hover:text-blue-600">Report</Link>
          <Link to="/login" className="block text-gray-700 hover:text-blue-600">Login</Link>
        </div>
      )}
    </nav>
  );
}
