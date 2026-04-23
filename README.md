# Autoffiliate 🚀

Automated TikTok Affiliate content management system. It scrapes trending products, generates viral scripts using Gemini 2.0, assembles videos via MoviePy, and publishes them to TikTok autonomously.

## 🛠️ Tech Stack
- **Core:** Python 3.11+
- **AI:** Gemini 2.0 Flash
- **Video Editing:** MoviePy 2.x / FFmpeg
- **Automation:** Playwright / Playwright-Stealth
- **Infrastructure:** Docker & Docker Compose

## 🏗️ Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Google Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey))
- TikTok Account & Kalodata Account

### 2. Initial Setup
1. Clone the repository.
2. Create and fill your `.env` file:
   ```env
   GEMINI_API_KEY=your_key_here
   KALODATA_EMAIL=your_email
   KALODATA_PASSWORD=your_password
   ```
3. Build the Docker environment:
   ```bash
   ./dc.sh build
   ```

### 3. Session Capture (Crucial)
To bypass bot detection on TikTok and Kalodata, you must capture a manual session once. Run these commands **locally** (on your host machine, not in Docker):

```bash
# Setup local environment for capture
python3 -m venv venv
source venv/bin/activate
pip install playwright playwright-stealth
playwright install chromium

# Capture sessions (Log in manually in the browser that opens)
python3 scripts/capture_session.py tiktok
python3 scripts/capture_session.py kalodata
```

### 4. Running the Engine
Once sessions are saved in `sessions/`, you can run the full automation pipeline:

```bash
./dc.sh run app python3 main.py
```

## 📂 Configuration
- **Niches:** Edit `config/niches/fashion.yaml` to change keywords, categories, and posting schedules.
- **Prompts:** Customize AI script behavior in `config/prompts/`.
- **Manual Mode:** If you want to use specific products without scraping, add `manual_products` to your niche YAML.

## 📜 Documentation
- [Low-Level Design (LLD)](docs/LLD.md)
- [Sprint Plan](agent_docs/sprint-plan.md) (Local)

## ⚠️ Known Issues & Bot Detection
Kalodata and TikTok have strong bot protections. If automation fails:
1. Refresh your sessions using `capture_session.py`.
2. Check `data/debug/` for screenshots of the failure.
3. Consider using `manual_products` in your config for 100% reliable posting.