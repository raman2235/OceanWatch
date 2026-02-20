export default function DashboardCards() {
  const stats = [
    { label: "Reports Today", value: 12 },
    { label: "Active Hazards", value: 3 },
    { label: "Verified Reports", value: 8 },
  ];

  return (
    <div className="space-y-4">
      {stats.map((s, i) => (
        <div
          key={i}
          className="bg-white p-4 rounded-xl shadow-md text-center"
        >
          <h4 className="text-gray-500">{s.label}</h4>
          <p className="text-2xl font-bold">{s.value}</p>
        </div>
      ))}
    </div>
  );
}
