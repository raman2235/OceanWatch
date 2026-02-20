import { useState, useEffect } from "react";

export default function ReportForm() {
  const [form, setForm] = useState({
    name: "",
    hazardType: "",
    description: "",
    media: null,
    latitude: "",
    longitude: "",
  });

  // Auto-fetch location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setForm((prev) => ({
          ...prev,
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        }));
      });
    }
  }, []);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (files) {
      setForm({ ...form, media: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Report submitted! Check console for values.");
    console.log(form);
    // Here you can integrate API POST request
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-50 py-12 px-4">
      <div className="max-w-2xl w-full bg-white p-8 rounded-2xl shadow-lg">
        <h2 className="text-3xl font-bold text-blue-900 mb-6 text-center">
          📝 Report Ocean Hazard
        </h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Your Name"
            value={form.name}
            onChange={handleChange}
            className="w-full border px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <select
            name="hazardType"
            value={form.hazardType}
            onChange={handleChange}
            className="w-full border px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          >
            <option value="">Select Hazard Type</option>
            <option value="High Waves">High Waves</option>
            <option value="Storm Surge">Storm Surge</option>
            <option value="Abnormal Tide">Abnormal Tide</option>
            <option value="Coastal Flooding">Coastal Flooding</option>
          </select>
          <textarea
            name="description"
            placeholder="Describe the hazard"
            value={form.description}
            onChange={handleChange}
            className="w-full border px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            rows={4}
            required
          ></textarea>
          <input type="file" name="media" onChange={handleChange} className="w-full" />

          {/* Editable Latitude and Longitude */}
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-gray-700">Latitude</label>
              <input
                type="number"
                name="latitude"
                value={form.latitude}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                step="0.0001"
                required
              />
            </div>
            <div className="flex-1">
              <label className="block text-gray-700">Longitude</label>
              <input
                type="number"
                name="longitude"
                value={form.longitude}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                step="0.0001"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-xl shadow-lg hover:bg-blue-700 transition"
          >
            Submit Report
          </button>
        </form>
      </div>
    </div>
  );
}
