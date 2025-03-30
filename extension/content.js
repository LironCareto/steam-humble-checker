// console.log("✅ Humble Tagger loaded!");
const url = "https://github.com/LironCareto/steam-humble-checker/humble-bundles.json";

const humbleBundles = {
    "September 2024": ["BeamNG.drive", "RimWorld"],
    "August 2024": ["Another Game"]
  };
  
  function normalizeTitle(title) {
    return title.trim().toLowerCase();
  }
  
  function checkAndTagGames() {
    const appLinks = document.querySelectorAll("a[href*='/app/']");
    console.log(`🎯 Found ${appLinks.length} app links`);
  
    appLinks.forEach(link => {
      const gameTitle = normalizeTitle(link.textContent);
      if (!gameTitle) return;
  
      for (const [month, games] of Object.entries(humbleBundles)) {
        if (games.map(normalizeTitle).includes(gameTitle)) {
          console.log(`✅ Match found: ${gameTitle} in ${month}`);
  
          // Prevent duplicates
          if (link.querySelector(".humble-tag")) return;
  
          const tag = document.createElement("div");
          tag.className = "humble-tag";
          tag.textContent = `🟣 Humble Choice ${month}`;
          tag.style.cssText = `
            position: absolute;
            top: 4px;
            right: 4px;
            background-color: #7e57c2;
            color: white;
            padding: 2px 6px;
            font-size: 11px;
            border-radius: 4px;
            z-index: 1000;
          `;
  
          // Make sure parent is positioned
          link.style.position = "relative";
          link.appendChild(tag);
          break;
        }
      }
    });
  }  
  
  window.addEventListener('load', () => {
    setTimeout(checkAndTagGames, 1000); // allow page to load
  });
  
