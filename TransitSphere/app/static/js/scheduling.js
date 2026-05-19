document.addEventListener("DOMContentLoaded", () => {
  const data = JSON.parse($("#scheduleData").textContent);
  new Chart($("#headwayChart"), {
    type: "bar",
    data: { labels: data.routes, datasets: [{ label: "Optimized headway minutes", data: data.headways, backgroundColor: "#34d399" }] },
    options: chartOptions()
  });
});
