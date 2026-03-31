(function () {
  const root = document.documentElement;
  const btn = document.getElementById("themeToggle");

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (btn) {
      const label = btn.querySelector(".label");
      if (label) label.textContent = theme === "light" ? "Light" : "Dark";
    }
  }

  const saved = localStorage.getItem("sk_theme");
  applyTheme(saved || "dark");

  if (btn) {
    btn.addEventListener("click", () => {
      const cur = root.getAttribute("data-theme") || "dark";
      const next = cur === "dark" ? "light" : "dark";
      localStorage.setItem("sk_theme", next);
      applyTheme(next);
    });
  }
})();
async function initNavbarTemp() {
  const tempEl = document.getElementById("skTemp");
  if (!tempEl) return;

  tempEl.textContent = "—°C";

  // geolocation best
  let coords = null;
  if ("geolocation" in navigator) {
    coords = await new Promise((resolve) => {
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
        () => resolve(null),
        { enableHighAccuracy: false, timeout: 8000, maximumAge: 600000 }
      );
    });
  }

  // if user blocks location -> keep —°C
  if (!coords) return;

  try {
    const res = await fetch(
      `/api/navbar-temp/?lat=${encodeURIComponent(coords.lat)}&lon=${encodeURIComponent(coords.lon)}`,
      { cache: "no-store" }
    );

    const data = await res.json();
    if (!data.ok || typeof data.temp !== "number") return;

    tempEl.textContent = `${data.temp.toFixed(1)}°C`;
  } catch (e) {
    // keep —°C
  }
}

document.addEventListener("DOMContentLoaded", initNavbarTemp);
