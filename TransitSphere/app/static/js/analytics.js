document.addEventListener("DOMContentLoaded", () => {
  const data = JSON.parse($("#forecastData").textContent);
  new Chart($("#forecastChart"), {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        { label: "Demand", data: data.demand, borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,.16)", fill: true, tension: .38 },
        { label: "Congestion", data: data.congestion, borderColor: "#fb7185", backgroundColor: "rgba(251,113,133,.12)", fill: true, tension: .38 }
      ]
    },
    options: chartOptions()
  });
  new Chart($("#riskChart"), {
    type: "doughnut",
    data: { labels: ["Delay probability", "Stable"], datasets: [{ data: [Math.max(...data.delay_probability), 100 - Math.max(...data.delay_probability)], backgroundColor: ["#fbbf24", "rgba(255,255,255,.14)"] }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#9aa8b8", boxWidth: 12 } } }
    }
  });
});
