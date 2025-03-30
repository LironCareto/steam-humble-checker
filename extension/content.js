// content.js
const DATA_URL = "https://raw.githubusercontent.com/LironCareto/steam-humble-checker/refs/heads/main/humble_bundles.json";

function normalizeTitle(title) {
  return title.trim().toLowerCase();
}

function createTag(label, color) {
  const tag = document.createElement("div");
  tag.className = "humble-tag";
  tag.textContent = label;
  tag.style.cssText = `
    position: absolute;
    top: 4px;
    right: 4px;
    background-color: ${color};
    color: white;
    padding: 2px 6px;
    font-size: 11px;
    border-radius: 4px;
    z-index: 1000;
  `;
  return tag;
}

function checkAndTagGames(bundleData) {
  console.log("✅ Loaded bundle data:", bundleData);

  function tryTagging(retries = 10) {
    let items = document.querySelectorAll("a[href*='/app/']");
    console.log("🎯 Found", items.length, "game links (using fallback selector)");
    if (items.length === 0 && retries > 0) {
      console.log("⏳ Waiting for game links to load...");
      return setTimeout(() => tryTagging(retries - 1), 1000);
    }

    items.forEach(titleElement => {
      const gameTitle = normalizeTitle(titleElement.innerText);
      for (const [bundleKey, games] of Object.entries(bundleData)) {
        const normalizedTitles = games.map(g => normalizeTitle(g.title));
        if (normalizedTitles.includes(gameTitle)) {
          const bundleType = games[0]?.type || "monthly";
const label = bundleType === "monthly"
  ? `🟦 Humble Choice ${bundleKey}`
  : `🟧 Humble Bundle (${bundleKey})`;
const color = bundleType === "monthly" ? "#2196f3" : "#ff9800";

          const bundle = games.find(g => normalizeTitle(g.title) === gameTitle);
const tag = document.createElement("a");
tag.href = bundle?.steam_url || "#";
tag.target = "_blank";
tag.rel = "noopener noreferrer";
tag.appendChild(createTag(label, color));
          titleElement.parentElement.style.position = "relative";
          titleElement.parentElement.appendChild(tag);
          break;
        }
      }
    });
  }

  tryTagging();
}

// Run on load and fetch the JSON
window.addEventListener('load', () => {
  console.log("🚀 Extension loaded. Waiting to fetch data...");
  setTimeout(() => {
    console.log("🌐 Fetching bundle data from:", DATA_URL);
    fetch(DATA_URL)
      .then(res => res.json())
      .then(json => checkAndTagGames(json))
      .catch(err => console.error("Failed to load humble bundles:", err));
  }, 1000);
});