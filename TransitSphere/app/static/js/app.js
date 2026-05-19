const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

$("#sidebarToggle")?.addEventListener("click", () => $("#sidebar")?.classList.toggle("collapsed"));
$("#themeToggle")?.addEventListener("click", () => {
  const root = document.documentElement;
  root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
});

$$("[data-counter]").forEach((el) => {
  const target = Number(el.dataset.counter);
  let value = 0;
  const step = Math.max(1, Math.ceil(target / 70));
  const timer = setInterval(() => {
    value = Math.min(target, value + step);
    el.textContent = value.toLocaleString();
    if (value === target) clearInterval(timer);
  }, 22);
});

function createBaseMap(id, zoom = 11) {
  const map = L.map(id, { zoomControl: false }).setView([12.9716, 77.5946], zoom);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);
  L.control.zoom({ position: "bottomright" }).addTo(map);
  return map;
}

function busIcon(status = "On Time") {
  const color = status === "Congested" ? "#fb7185" : status === "Delayed" ? "#fbbf24" : "#38bdf8";
  return L.divIcon({
    className: "",
    html: `<div class="bus-marker" style="background:${color}"><i class="bi bi-bus-front-fill"></i></div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  });
}

function showToast(title, body) {
  const dock = $("#toastDock");
  if (!dock) return;
  const node = document.createElement("div");
  node.className = "live-toast";
  node.innerHTML = `<b>${title}</b><div>${body}</div>`;
  dock.appendChild(node);
  setTimeout(() => node.remove(), 5200);
}

async function getJSON(url) {
  const response = await fetch(url);
  return response.json();
}

function chartOptions(extra = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: "#9aa8b8", boxWidth: 12 } },
      ...(extra.plugins || {}),
    },
    scales: {
      x: { ticks: { color: "#9aa8b8" }, grid: { color: "rgba(255,255,255,.08)" } },
      y: { ticks: { color: "#9aa8b8" }, grid: { color: "rgba(255,255,255,.08)" } },
      ...(extra.scales || {}),
    },
    ...extra,
  };
}
