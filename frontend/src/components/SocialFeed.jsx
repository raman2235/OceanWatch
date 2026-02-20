export default function SocialFeed() {
  const posts = [
    { user: "User123", text: "High waves observed near Chennai coast!" },
    { user: "User456", text: "Unusual tide levels reported in Kerala." },
  ];

  return (
    <div className="bg-white p-4 rounded-xl shadow-md">
      <h3 className="text-lg font-semibold mb-3">Live Social Media Feed</h3>
      <ul className="space-y-3">
        {posts.map((p, i) => (
          <li key={i} className="border-b pb-2">
            <strong>@{p.user}:</strong> {p.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
