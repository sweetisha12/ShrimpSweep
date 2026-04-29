# Shrimp Sweep

An underwater Pac-Man style game built in Python for the browser with PyScript.

## Included Features

- 3 levels with increasing difficulty
- Easy, medium, and hard question gates
- 3-correct-in-a-row rule before each level
- Reset back to easy on a failed question
- Slower shrimp and faster squid as levels increase
- More bomb-cherries each level
- High score saved in browser storage
- Custom level-complete messages
- Shared leaderboard support through Google Apps Script
- Layout designed to be embedded into Google Sites

## Files To Edit Later

- `game_content.py`
  - Replace the 30 placeholder questions in `QUESTIONS`
  - Update the post-level text in `LEVEL_MESSAGES`
- `settings.py`
  - Paste your deployed Google Apps Script URL into `LEADERBOARD_ENDPOINT`

## How The Leaderboard Works

This project supports two modes:

1. Local fallback mode
   - Scores are stored in browser `localStorage`
   - Useful while developing
2. Shared mode
   - Scores are stored through a Google Apps Script web app
   - This is the mode to use when many people are playing from Google Sites

## Google Sites Deployment

Google Sites cannot directly host arbitrary Python app files by itself, so the practical setup is:

1. Host this folder as a static site somewhere public
   - GitHub Pages is the simplest option
   - A Google Apps Script web app can also serve the files if you want to keep it in Google tools
2. Embed the hosted game URL into Google Sites using the `Embed` option
3. If you want a shared leaderboard, deploy the Apps Script in `google_apps_script/Code.gs`
4. Paste the Apps Script web app URL into `settings.py`

## Quick Start

Open `index.html` in a browser that supports PyScript hosting, or serve the folder with a static file server.

Example local server:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000/underwater-pacman/`.
