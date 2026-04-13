(function () {
  const THEME_KEY = "sk_theme";

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    const label = document.getElementById("themeLabel");
    if (label) label.textContent = theme === "light" ? "Light" : "Dark";
  }

  function initTheme() {
    const saved = localStorage.getItem(THEME_KEY) || "dark";
    applyTheme(saved);

    const btn = document.getElementById("themeToggle");
    if (btn) {
      btn.addEventListener("click", () => {
        const current = localStorage.getItem(THEME_KEY) || "dark";
        const next = current === "dark" ? "light" : "dark";
        localStorage.setItem(THEME_KEY, next);
        applyTheme(next);
      });
    }
  }

  async function fetchWeather(lat, lon) {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m`;
    const res = await fetch(url);
    const data = await res.json();
    const t = data?.current?.temperature_2m;
    return (typeof t === "number") ? t : null;
  }

  function initWeather() {
    const el = document.getElementById("weatherTemp");
    if (!el) return;

    if (!navigator.geolocation) {
      el.textContent = "--°C";
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const { latitude, longitude } = pos.coords;
          const temp = await fetchWeather(latitude, longitude);
          el.textContent = (temp === null) ? "--°C" : `${temp.toFixed(1)}°C`;
        } catch (e) {
          el.textContent = "--°C";
        }
      },
      () => {
        el.textContent = "--°C";
      },
      { enableHighAccuracy: false, timeout: 7000, maximumAge: 600000 }
    );
  }

  document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initWeather();
  });
})();
