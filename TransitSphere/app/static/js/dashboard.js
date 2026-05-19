let miniMap;
let miniMarkers = {};

async function initDashboard() {
  miniMap = createBaseMap("miniMap", 11);
  const routes = await getJSON("/api/routes?featured=1&limit=18");
  for (const route of routes) {
    const detail = await getJSON(`/api/route/${route.route_id}`);
    L.polyline(detail.shape, { color: `#${route.route_color}`, weight: 4, opacity: .72 }).addTo(miniMap);
  }
  const forecast = await getJSON("/api/analytics/forecast");
  new Chart($("#demandChart"), {
    type: "line",
    data: { labels: forecast.labels, datasets: [{ label: "Predicted demand", data: forecast.demand, borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,.18)", fill: true, tension: .38 }] },
    options: chartOptions()
  });
  new Chart($("#routeChart"), {
    type: "bar",
    data: { labels: ["500D", "356C", "335E", "KIA-8", "201R", "V-500CA"], datasets: [{ label: "Utilization %", data: [91, 84, 76, 69, 72, 88], backgroundColor: ["#38bdf8", "#34d399", "#fbbf24", "#a78bfa", "#fb7185", "#22c55e"] }] },
    options: chartOptions()
  });
  const weather = await getJSON("/api/weather");
  $("#weatherCard").innerHTML = `<h3>Weather impact</h3><div class="d-flex align-items-center gap-3"><i class="bi bi-cloud-rain fs-2 text-info"></i><div><strong>${weather.temperature}°C · ${weather.condition}</strong><p class="mb-0 text-secondary">${weather.rainfall} mm rainfall · ${weather.impact}</p></div></div>`;
  connectRealtime(updateDashboard);
}

function updateDashboard(state) {
  Object.entries(state.kpis).forEach(([key, value]) => {
    const node = $(`#kpi-${key}`);
    if (node) node.textContent = value;
  });
  state.buses.forEach((bus) => {
    const marker = miniMarkers[bus.bus_id] || L.marker([bus.lat, bus.lng], { icon: busIcon(bus.status) }).addTo(miniMap);
    marker.setLatLng([bus.lat, bus.lng]).setIcon(busIcon(bus.status)).bindPopup(`<b>${bus.bus_id}</b><br>${bus.route_name}<br>${bus.occupancy}% occupied`);
    miniMarkers[bus.bus_id] = marker;
  });
}

function connectRealtime(handler) {
  if (window.io) {
    const socket = io();
    socket.on("transport_update", handler);
  }
  setInterval(async () => handler(await getJSON("/api/simulation/state")), 4000);
}

document.addEventListener("DOMContentLoaded", initDashboard);
