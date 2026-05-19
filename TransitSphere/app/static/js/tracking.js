let trackingMap;
const busMarkers = {};
const routeLayers = {};

async function initTracking() {
  trackingMap = createBaseMap("trackingMap", 12);
  const routes = await getJSON("/api/routes?featured=1&limit=18");
  for (const route of routes) {
    const detail = await getJSON(`/api/route/${route.route_id}`);
    routeLayers[route.route_id] = L.polyline(detail.shape, { color: `#${route.route_color}`, weight: 5, opacity: .78 }).addTo(trackingMap);
    detail.stops.forEach((stop) => L.circleMarker([stop.lat, stop.lng], {
      radius: 5 + stop.density / 28, color: "#ffffff", weight: 1, fillColor: "#34d399", fillOpacity: .75
    }).addTo(trackingMap).bindPopup(`<b>${stop.stop_name}</b><br>Passenger density ${stop.density}%`));
  }
  $("#routeFilter").addEventListener("change", filterRoutes);
  connectTracking();
}

function filterRoutes() {
  const selected = $("#routeFilter").value;
  Object.entries(routeLayers).forEach(([id, layer]) => {
    if (!selected || selected === id) layer.addTo(trackingMap);
    else trackingMap.removeLayer(layer);
  });
}

function connectTracking() {
  const handler = (state) => {
    const selected = $("#routeFilter").value;
    const list = $("#fleetList");
    list.innerHTML = "";
    state.buses.filter((bus) => !selected || bus.route_id === selected).forEach((bus) => {
      const popup = `<b>${bus.bus_id}</b><br>Route ${bus.route_name}<br>Occupancy ${bus.occupancy}%<br>Speed ${bus.speed} km/h<br>Delay ${bus.delay} min<br>Status ${bus.status}<br>Next: ${bus.next_stop}`;
      const marker = busMarkers[bus.bus_id] || L.marker([bus.lat, bus.lng], { icon: busIcon(bus.status) }).addTo(trackingMap);
      marker.setLatLng([bus.lat, bus.lng]).setIcon(busIcon(bus.status)).bindPopup(popup);
      busMarkers[bus.bus_id] = marker;
      const item = document.createElement("div");
      item.className = "fleet-item";
      item.innerHTML = `<b>${bus.bus_id} &middot; ${bus.route_name}</b><small>${bus.status} &middot; ${bus.occupancy}% occupied &middot; ${bus.delay} min delay</small>`;
      item.onclick = () => { trackingMap.flyTo([bus.lat, bus.lng], 14); marker.openPopup(); };
      list.appendChild(item);
    });
  };
  if (window.io) io().on("transport_update", handler);
  setInterval(async () => handler(await getJSON("/api/simulation/state")), 3500);
}

document.addEventListener("DOMContentLoaded", initTracking);
