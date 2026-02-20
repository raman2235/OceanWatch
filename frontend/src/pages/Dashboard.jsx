import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "leaflet.heat";
import { useEffect } from "react";

// Fix Leaflet default icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Sample hazard reports
const reports = [
  { id: 1, latitude: 13.0827, longitude: 80.2707, hazardType: "High Waves" },
  { id: 2, latitude: 9.9312, longitude: 76.2673, hazardType: "Abnormal Tide" },
  { id: 3, latitude: 18.5204, longitude: 73.8567, hazardType: "Storm Surge" },
  { id: 4, latitude: 19.076, longitude: 72.8777, hazardType: "High Waves" },
  { id: 5, latitude: 21.1458, longitude: 79.0882, hazardType: "Abnormal Tide" },
];

// Component to add heatmap
function Heatmap({ reports }) {
  const map = useMap();
  useEffect(() => {
    const heatPoints = reports.map((r) => [r.latitude, r.longitude, 1]);
    const heat = L.heatLayer(heatPoints, { radius: 25, blur: 15 });
    heat.addTo(map);

    return () => {
      map.removeLayer(heat);
    };
  }, [map, reports]);

  return null;
}

export default function Dashboard() {
  // Sample stats
  const stats = [
    { label: "Reports Today", value: reports.length },
    { label: "Active Hazards", value: 3 },
    { label: "Verified Reports", value: 2 },
  ];

  // Sample social posts
  const posts = [
    { user: "User123", text: "High waves observed near Chennai coast!" },
    { user: "User456", text: "Unusual tide levels reported in Kerala." },
  ];

  return (
    <div className="min-h-screen p-6 bg-blue-50">
      <h2 className="text-3xl font-bold text-blue-900 mb-6">📊 Dashboard</h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left side: Map + Social Feed */}
        <div className="lg:col-span-2 space-y-6">
          {/* Map */}
          <div className="rounded-xl overflow-hidden shadow-lg">
            <MapContainer
              center={[20.5937, 78.9629]}
              zoom={5}
              scrollWheelZoom={true}
              style={{ height: "400px", width: "100%" }} // ensure height
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {/* Render all hazard markers */}
              {reports.map((r) => (
                <Marker key={r.id} position={[r.latitude, r.longitude]}>
                  <Popup>{r.hazardType}</Popup>
                </Marker>
              ))}

              {/* Heatmap */}
              <Heatmap reports={reports} />
            </MapContainer>
          </div>

          {/* Social Feed */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-xl font-semibold mb-4">Live Social Media Feed</h3>
            <ul className="space-y-3">
              {posts.map((p, i) => (
                <li key={i} className="border-b pb-2">
                  <strong>@{p.user}:</strong> {p.text}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Right side: Stats Cards */}
        <div className="space-y-4">
          {stats.map((s, i) => (
            <div
              key={i}
              className="bg-white p-6 rounded-xl shadow-md text-center hover:shadow-lg transition"
            >
              <h4 className="text-gray-500">{s.label}</h4>
              <p className="text-2xl font-bold text-blue-800">{s.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
