import { useState } from "react";

export default function ReportForm() {
  const [form, setForm] = useState({
    name: "",
    location: "",
    type: "",
    media: null,
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setForm({ ...form, [name]: files ? files[0] : value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Report submitted:", form);
    alert("✅ Report submitted (check console for data)");
  };

  return (
    <div className="max-w-md mx-auto bg-white shadow-md rounded-xl p-6 mt-6">
      <h3 className="text-xl font-semibold mb-4">Report an Ocean Hazard</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="name"
          placeholder="Your Name"
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded-md"
        />
        <input
          type="text"
          name="location"
          placeholder="Location"
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded-md"
        />
        <select
          name="type"
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded-md"
        >
          <option value="">Select Hazard Type</option>
          <option value="tsunami">Tsunami</option>
          <option value="waves">High Waves</option>
          <option value="surge">Storm Surge</option>
          <option value="flood">Flooding</option>
        </select>
        <input
          type="file"
          name="media"
          onChange={handleChange}
          className="w-full"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
        >
          Submit Report
        </button>
      </form>
    </div>
  );
}
