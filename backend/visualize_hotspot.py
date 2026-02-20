import folium

# === API se mila hua sample response ===
hotspots = [
    {"cell_lat": 25.1, "cell_lon": 78.06, "count": 2},
    {"cell_lat": 25.12, "cell_lon": 79.22, "count": 2}
]

# === Map center (average lat/lon se) ===
center_lat = sum(h["cell_lat"] for h in hotspots) / len(hotspots)
center_lon = sum(h["cell_lon"] for h in hotspots) / len(hotspots)

# === Folium map banaya ===
m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

# === Har hotspot ko marker add karna ===
for h in hotspots:
    folium.CircleMarker(
        location=[h["cell_lat"], h["cell_lon"]],
        radius=5 + h["count"]*2,   # count ke hisaab se size
        popup=f"Count: {h['count']}",
        color="red",
        fill=True,
        fill_color="red"
    ).add_to(m)

# === Map save to HTML file ===
m.save("hotspots_map.html")
print("✅ Map saved as hotspots_map.html. Open it in browser!")

