import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-blue-50 to-blue-100">
      
      {/* Hero Section */}
      <section className="flex-1 flex flex-col items-center justify-center text-center px-6 py-16">
        <h1 className="text-4xl md:text-5xl font-extrabold text-blue-900 mb-4">
          🌊 Ocean Hazard Reporting Platform
        </h1>
        <p className="text-lg md:text-xl text-gray-700 max-w-2xl mb-8">
          A unified platform to report real-time ocean hazards, visualize social
          media discussions, and support disaster management agencies in making
          informed decisions.
        </p>
        <div className="flex gap-4 flex-wrap justify-center">
          <Link
            to="/report"
            className="bg-blue-600 text-white px-6 py-3 rounded-xl shadow-lg hover:bg-blue-700 transition"
          >
            Report a Hazard
          </Link>
          <Link
            to="/dashboard"
            className="bg-white text-blue-600 px-6 py-3 rounded-xl shadow-md border hover:bg-gray-50 transition"
          >
            View Dashboard
          </Link>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="bg-white py-12 shadow-inner">
        <div className="max-w-5xl mx-auto px-6 grid md:grid-cols-3 gap-8 text-center">
          <div className="p-6 bg-blue-50 rounded-xl shadow hover:shadow-md transition">
            <h3 className="text-xl font-bold text-blue-800 mb-2">📍 Geo-tagged Reports</h3>
            <p className="text-gray-600">
              Citizens can submit location-based hazard reports with photos or videos.
            </p>
          </div>
          <div className="p-6 bg-blue-50 rounded-xl shadow hover:shadow-md transition">
            <h3 className="text-xl font-bold text-blue-800 mb-2">📊 Social Media Analytics</h3>
            <p className="text-gray-600">
              Track hazard-related conversations and sentiment from Twitter, YouTube, and more.
            </p>
          </div>
          <div className="p-6 bg-blue-50 rounded-xl shadow hover:shadow-md transition">
            <h3 className="text-xl font-bold text-blue-800 mb-2">⚡ Real-time Dashboard</h3>
            <p className="text-gray-600">
              Interactive map with dynamic hotspots and verified hazard alerts.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
