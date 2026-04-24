# Autoffiliate 🚀 (Semi-Auto Edition)

Semi-automated TikTok Affiliate content engine. It transforms product exports (TCC or Kalodata) into high-quality videos using Gemini 2.0 and MoviePy, preparing everything for manual posting to ensure maximum account safety.

## 🛠️ Tech Stack
- **Core:** Python 3.11+
- **AI:** Gemini 2.0 Flash (Scripting)
- **Video Editing:** MoviePy 2.x / FFmpeg
- **Data Parsing:** Pandas / Openpyxl (Universal Parser)
- **Infrastructure:** Docker & Docker Compose

## 🏗️ Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Google Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey))

### 2. Initial Setup
1. Clone the repository.
2. Create and fill your `.env` file:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
3. Build the Docker environment:
   ```bash
   ./dc.sh build
   ```

## 🔄 The Semi-Auto Workflow

### Step 1: Sourcing Data (Free Methods)

You can choose one of these two free methods to source products:

#### Method A: TikTok Shop Marketplace (Recommended)
1. Open your **TikTok App** or **TikTok Shop Seller Center**.
2. Go to the **Affiliate Marketplace**.
3. Find products in your niche with high sales and good commissions.
4. Copy the product details (Title, Price, Image URL) into `data/input/manual_template.csv`.
   - *Tip: Right-click a product image in the browser and select "Copy Image Address" to get the URL.*

#### Method B: TikTok Creative Center (Batch Export)
1. Open [TikTok Creative Center - Top Products](https://ads.tiktok.com/business/creativecenter/inspiration/top-products/pc/en?region=ID).
2. Filter by Category and Region (Indonesia).
3. Open **Browser Console** (Press `F12` or `Ctrl+Shift+J`).
4. Copy the contents of `scripts/tcc_exporter.js` from this project.
5. Paste it into the Console and press **Enter**.
6. A CSV file will be downloaded automatically. Place it into `data/input/`.

---

### Step 2: Generation (Automated)
Run the engine to process the files and generate videos:
```bash
./dc.sh up
```
The system will:
- Parse all files in `data/input/` (supports TCC, TikTok Shop Marketplace, etc.).
- Use Gemini to write viral scripts based on product titles.
- Download product images.
- Render unique videos.
- Organize everything into "Post Packages".

### Step 3: Posting (Manual)
1. Navigate to `data/output/{date}/`.
2. Find the folder for your product.
3. Use the `video.mp4` and `caption.txt` provided to post manually on TikTok.

## 📂 Directory Structure
- `data/input/`: Place your CSV/Excel files here (use `manual_template.csv` for manual entry).
- `data/output/`: Your ready-to-post videos and captions will appear here.
- `scripts/`: Contains the `tcc_exporter.js` browser script.
- `config/niches/`: Configure niche-specific settings (tone, language, hashtags).

## 📜 Documentation
- [Low-Level Design (LLD)](docs/LLD.md)
- [MVP Specification](docs/AUTOFFILIATE_MVP.md)
- [Sprint Plan](agent_docs/sprint-plan.md) (Local)

## ⚠️ Advantages of Semi-Auto
- **100% Free Research**: Use official TikTok tools (Marketplace & TCC) instead of expensive paid scrapers.
- **Minimal Cost**: Only pay for the Gemini API (usage-based).
- **100% Safety**: No automated login/posting means zero risk of bot detection bans.
- **High Efficiency**: System handles the 30-minute creative tasks (scripting/editing).