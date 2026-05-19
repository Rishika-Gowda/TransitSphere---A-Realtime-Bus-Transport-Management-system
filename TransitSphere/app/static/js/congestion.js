document.addEventListener("DOMContentLoaded", async () => {
  const map = createBaseMap("congestionMap", 12);
  const dashboard = await getJSON("/api/dashboard");
  const heat = dashboard.congestion.map((h) => [h.lat, h.lng, h.intensity]);
  L.heatLayer(heat, { radius: 38, blur: 26, maxZoom: 13, gradient: { .35: "#38bdf8", .6: "#fbbf24", .9: "#fb7185" } }).addTo(map);
  dashboard.congestion.forEach((h) => {
    L.circle([h.lat, h.lng], { radius: 650 + h.intensity * 800, color: "#fb7185", fillColor: "#fb7185", fillOpacity: .18 })
      .addTo(map).bindPopup(`<b>${h.name}</b><br>${Math.round(h.intensity * 100)}% traffic intensity<br>${h.delay} min delay`);
  });
});
