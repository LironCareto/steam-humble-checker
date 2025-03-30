# Steam Wishlist Humble Tagger

A lightweight Chrome extension that tags games in your Steam wishlist if they have appeared in past **Humble Choice** bundles — helping you avoid buying something you already have access to.

## 🧠 Why?

As a Humble Choice subscriber, it's easy to lose track of which games you've already claimed. This extension cross-references your Steam wishlist with past bundles and shows a small badge directly on your wishlist page.

## 🖥 Features

- ✅ Automatically scans your Steam wishlist
- 🏷 Adds a badge to any game included in past Humble Choice bundles
- 🌐 Supports dynamic Steam layouts
- 🔄 Fetches bundle data from a centralized, public JSON file (hosted on GitHub Pages)

## 📦 How to Install (Dev Mode)

1. Clone or download this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable **Developer Mode** (top right)
4. Click **“Load unpacked”** and select the project folder
5. Open your [Steam Wishlist](https://store.steampowered.com/wishlist/)
6. Games that have appeared in Humble Choice will now be tagged!

## 🔁 Updating Bundle Data

This extension loads game data from a hosted JSON file. You can update `humble_bundles.json` and push it to your GitHub Pages site. The extension will automatically fetch the latest version.

> 🧠 If you're using a local version of the JSON file, make sure to update your `manifest.json` and use `chrome.runtime.getURL("humble_bundles.json")` in `content.js`.

## 📄 License

This project is open-source under the [MIT License](LICENSE).  
You are free to use, modify, and distribute it. Contributions welcome!

## 🚀 Roadmap Ideas

- [ ] Support fuzzy matching for slightly different game titles
- [ ] Allow showing claimed bundles in a popup
- [ ] Detect owned games in your Steam library
- [ ] Publish to Chrome Web Store

---

Made with ☕ and too many unplayed games.
