# Autoffiliate

Automated TikTok Affiliate content management system using Kalodata intelligence and Gemini 2.0 reasoning.

## 🚀 Overview
Autoffiliate is designed to scale TikTok Affiliate operations by automating the entire pipeline from product discovery to content generation and posting. It supports multiple niches through a modular configuration system.

## 🛠️ Tech Stack
- **Core:** Python 3.11+
- **AI:** Gemini 2.0 (Google GenAI SDK)
- **Scraping:** Playwright
- **Video Editing:** MoviePy / FFmpeg
- **Containerization:** Docker & Docker Compose

## 🏗️ Getting Started

### Prerequisites
- Docker & Docker Compose
- Google Gemini API Key

### Setup
1. Copy `.env.example` to `.env` and fill in your keys.
2. Initialize the environment:
   ```bash
   ./dc.sh build
   ```
3. Run the application:
   ```bash
   ./dc.sh up
   ```

## 📂 Project Structure
- `config/niches/`: YAML configurations for different product niches.
- `docs/`: System documentation (LLD and Feature Specs).
- `src/`: Source code for the automation pipeline.

## 📜 Documentation
- [Feature Specification: Autoffiliate MVP](docs/AUTOFFILIATE_MVP.md)
- [Low-Level Design (LLD)](docs/LLD.md)