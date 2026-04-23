# Feature Specification: Autoffiliate MVP

## 1. Overview
Autoffiliate is an automated content management system designed for scaling TikTok Affiliate operations. It leverages Kalodata for market intelligence and Gemini 2.0 for creative reasoning to produce and post high-quality, unique affiliate content at scale.

## 2. Problem Statement
Manual content creation is the primary bottleneck for scaling TikTok Affiliate accounts. Managing multiple niches requires significant time and carries a high risk of "unoriginal content" flags or shadowbans if content is repetitive.

## 3. Goals & Objectives
- **Scalability:** Enable a single user to manage multiple niche-specific accounts with zero daily manual intervention.
- **Originality:** Ensure every video is perceived as unique by TikTok's algorithm through dynamic asset variation.
- **Efficiency:** Automate the entire pipeline from product discovery (Kalodata) to script writing (Gemini) to final posting.
- **Modular Design:** Build a core engine that can be easily extended to new niches (Fashion, Home, Gadgets, etc.) via configuration.

## 4. Target Audience
- **Primary Persona:** Professional TikTok Affiliate marketers focused on high-volume scaling.
- **Pilot Niche:** Fashion (chosen for high impulse-buy potential).

## 5. Functional Requirements (MVP)

### FR-1: Automated Product Discovery (Kalodata)
- **Description:** System must fetch trending, high-conversion products from Kalodata within the target niche.
- **Priority:** Must Have
- **Acceptance Criteria:** Successfully retrieves a daily list of top 10 products with their metadata (URL, price, sales volume).

### FR-2: Gemini-Powered Scripting Engine
- **Description:** Use Gemini 2.0 to generate unique, persuasive scripts for each product.
- **Priority:** Must Have
- **Acceptance Criteria:** Generates 3 unique script variations per product to avoid pattern detection.

### FR-3: Multi-Niche Architecture
- **Description:** The system must support niche-specific configurations via the `config/niches/` directory.
- **Priority:** Must Have (Added per User Request)
- **Acceptance Criteria:** Adding a new YAML file to `config/niches/` allows the system to manage a new niche without code modifications.

### FR-4: Video Assembly & Asset Variation
- **Description:** Combine product assets with AI-generated text, dynamic music, and random transitions.
- **Priority:** Must Have
- **Acceptance Criteria:** Each video produced has a unique hash and visual sequence to bypass MD5/visual matching filters.

### FR-5: Daily Scheduler & Posting
- **Description:** Automatically post 3 videos per day to the target TikTok account at optimal times.
- **Priority:** Must Have
- **Acceptance Criteria:** 100% automated posting for the first 30 days of the pilot.

### NFR-1: Safety & Anti-Spam
- **Description:** Implement rate-limiting, human-like delays, and visual randomization to protect accounts.
- **Priority:** Must Have

### NFR-2: Containerization (Docker)
- **Description:** Project must be fully dockerized with a standard `dc.sh` wrapper.
- **Priority:** Must Have (Added per User Request)

### NFR-3: Observability
- **Description:** Detailed logs for each pipeline stage (Scrape -> Script -> Render -> Post).
- **Priority:** Must Have

## 7. Success Metrics
- **Consistency:** 90 videos posted in 30 days without manual touch.
- **Growth:** Minimum 1,000 views on 10% of videos (organic).
- **Security:** Zero "Unoriginal Content" violations on the pilot account.

## 8. Out of Scope (Post-MVP)
- Automated comment management.
- Direct CRM integration.
- Live stream automation.
