# 📊 LensOfFinance AI

**Smart AI-Powered Stock Market Insights, News Intelligence & Pattern Detection.**  
_Elevate your investment decisions with emotion-aware sentiment analysis, pattern recognition, and deep market context._

---

## 🚀 Overview

**LensOfFinance AI** is a full-stack intelligent market analysis engine built with **FastAPI**, **MongoDB**, and **PostgreSQL**, leveraging **transformer-based NLP models** and advanced **candlestick pattern detection** to provide a new lens for financial decision-making.

This platform is tailored for **retail investors**, **quant researchers**, and **fintech developers**, combining the best of:

- 📈 Technical Chart Patterns
- 📰 AI-Powered News Sentiment
- 🧠 Deep Company Fundamentals
- 🗣️ Social & Behavioral Signals *(coming soon)*

---

## 🧠 Features

### 📌 Pattern Recognition Engine (Candlestick)

- Analyzes historical OHLCV data
- Detects and stores multiple single-candle patterns per stock per day
- Scalable architecture: Separate table per stock + global common table
- Fast filter/search API by `date`, `symbol`, and `pattern combinations`

> 🔒 Bitwise encoding is used internally for efficient pattern representation and search – not disclosed here for intellectual protection.

---

### 📰 Real-Time News + Sentiment API

- Fetches news from **Google News RSS**
- Extracts full article content using **Newspaper3k**
- Runs **transformer-based sentiment analysis** (`distilbert`)
- Auto-summarizes headlines and body using **BART/CNN** summarizer
- Returns latest sentiment-marked, summarized news for any stock

---

### 📂 Company Intelligence API

- Pulls detailed per-stock data like:
  - Income Statement
  - Balance Sheet
  - Cash Flow
  - Pros & Cons (automated)
  - About Section
- Fully searchable by symbol
- Stored efficiently in **MongoDB Atlas**

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Backend | FastAPI, Python |
| Databases | PostgreSQL (candlestick DB), MongoDB (news + fundamentals) |
| ML/NLP | Transformers (Hugging Face), BART, DistilBERT, Newspaper3k |
| ETL | Pandas, Requests, TA-Lib |
| DevOps | `.env`, Docker (WIP), Logging |

---

## 📡 Core APIs

### `GET /patterns/latest`
Fetch latest detected patterns across stocks.

### `GET /patterns/search`
Search by `symbol`, `pattern_value`, and date range.

### `GET /stock/{symbol}`
Retrieve OHLCV + matched patterns for a single stock.

### `GET /company/{symbol}`
Get detailed company financials and summary.

### `GET /news/{symbol}`
Fetch latest AI-processed news for the company.

---

## 🧱 Database Design (Overview)

### PostgreSQL

- `common_stock_data`: All pattern matches across stocks.
- `stock_<symbol>`: One table per company for faster lookup & indexing.

### MongoDB

- Collection: `companies`
  - Stores financials, news sentiment, pros/cons, and summaries per stock.

---

## 🔐 Security

- All APIs protected via **API key header**: `x-api-key`
- Rate-limiting and abuse monitoring (coming soon)

---

## 🧑‍💻 Developer Notes

- Async-first FastAPI for high performance
- Modular structure (routers, models, services, database)
- Pydantic schemas for strict API contracts
- Readable logging and model loading on startup

---

## 🌍 Vision

> **LensOfFinance AI** aims to become the **AI-powered financial lens** for every trader and investor — merging patterns, behavior, and emotion with hard data.

---

## 📬 Connect

If you're a recruiter, investor, or developer interested in collaboration:

- **GitHub**: [github.com/Vipul4765](https://github.com/Vipul4765)
- **LinkedIn**: [linkedin.com/in/vipuldhankar](https://www.linkedin.com/in/vipul-kumar-5861221b9/)
- **Email**: vipuldhankar17170277@gmail.com

---

## ✅ Status: `In Active Development 🚧`

Next milestones:

- Social sentiment from Twitter/X
- Backtesting & performance scoring
- Real-time pattern alert system
- AI voice assistant for market queries

---

> 📢 _This project is 100% original. Do not replicate or redistribute without permission.
> *Built with passion, by Vipul Dhankar 🔥*

