from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any
from models import NewsItem, CompanyData
from dotenv import load_dotenv
from transformers import pipeline
from newspaper import Article
from dateutil import parser as dateparser
import feedparser
import logging
import os
from datetime import datetime

# Load .env
load_dotenv()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB credentials
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@cluster0.8gyw646.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# DB connection
client = AsyncIOMotorClient(uri)
db = client["additional_information"]
collection = db["companies"]

# FastAPI app
app = FastAPI()

# ML pipelines (global)
sentiment_model = None
summarizer = None

SENTIMENT_MODEL_NAME = os.getenv("SENTIMENT_MODEL", "distilbert/distilbert-base-uncased-finetuned-sst-2-english")
SUMMARIZER_MODEL_NAME = os.getenv("SUMMARIZER_MODEL", "sshleifer/distilbart-cnn-12-6")

@app.on_event("startup")
async def startup_event():
    global sentiment_model, summarizer
    logger.info("Loading sentiment and summarization models...")
    try:
        sentiment_model = pipeline("sentiment-analysis", model=SENTIMENT_MODEL_NAME)
        summarizer = pipeline("summarization", model=SUMMARIZER_MODEL_NAME)
        logger.info("✅ Models loaded successfully.")
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        raise

@app.get("/companies", response_model=List[str])
async def list_symbols():
    doc = await collection.find_one({}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="No companies found.")
    return list(doc.keys())

@app.get("/company/{symbol}", response_model=CompanyData)
async def get_company_data(symbol: str):
    symbol = symbol.upper()
    doc = await collection.find_one({}, {symbol: 1, "_id": 0})
    if not doc or symbol not in doc:
        raise HTTPException(status_code=404, detail="Company not found")
    return doc[symbol]

async def get_company_field(symbol: str, field: str, error_message: str):
    symbol = symbol.upper()
    doc = await collection.find_one({}, {f"{symbol}.{field}": 1, "_id": 0})
    try:
        return doc[symbol][field]
    except Exception:
        raise HTTPException(status_code=404, detail=error_message)

@app.get("/company/{symbol}/income_statement", response_model=List[Dict[str, Any]])
async def get_income_statement(symbol: str):
    return await get_company_field(symbol, "income_statement", "Income statement not found")

@app.get("/company/{symbol}/balance_sheet", response_model=List[Dict[str, Any]])
async def get_balance_sheet(symbol: str):
    return await get_company_field(symbol, "balance_sheet", "Balance sheet not found")

@app.get("/company/{symbol}/cash_flow", response_model=List[Dict[str, Any]])
async def get_cash_flow(symbol: str):
    return await get_company_field(symbol, "cash_flow", "Cash flow not found")

@app.get("/company/{symbol}/pros", response_model=List[str])
async def get_pros(symbol: str):
    return await get_company_field(symbol, "pros", "Pros not found")

@app.get("/company/{symbol}/cons", response_model=List[str])
async def get_cons(symbol: str):
    return await get_company_field(symbol, "cons", "Cons not found")

@app.get("/company/{symbol}/about", response_model=str)
async def get_about(symbol: str):
    return await get_company_field(symbol, "about", "About info not found")

@app.get("/news/{symbol}", response_model=List[NewsItem])
def get_latest_news(symbol: str):
    query = symbol.replace("&", "and").replace("-", " ")
    rss_url = f"https://news.google.com/rss/search?q={query}+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
    logger.info(f"Fetching news for {query}")

    try:
        feed = feedparser.parse(rss_url)
        if feed.bozo:
            raise Exception(feed.bozo_exception)
        entries = feed.entries
    except Exception as e:
        logger.error(f"RSS feed error for {query}: {e}")
        raise HTTPException(status_code=503, detail="Unable to fetch news")

    articles = []

    for entry in entries[:3]:
        try:
            title = getattr(entry, "title", "No Title")
            link = getattr(entry, "link", "")
            published_str = getattr(entry, "published", None)

            published_dt = dateparser.parse(published_str) if published_str else datetime.utcnow()

            # Extract full article
            full_text = ""
            try:
                article = Article(link)
                article.download()
                article.parse()
                full_text = article.text.strip()
            except Exception as e:
                logger.warning(f"Article extraction failed for {link}: {e}")

            text_to_use = full_text if len(full_text) > 100 else title

            # Sentiment
            sentiment = "NEUTRAL"
            try:
                sentiment_result = sentiment_model(text_to_use)[0]
                sentiment = sentiment_result.get("label", "NEUTRAL")
            except Exception as e:
                logger.error(f"Sentiment error: {e}")

            # Summary
            summary = title
            try:
                summary_result = summarizer(text_to_use, max_length=80, min_length=25, do_sample=False)[0]
                summary = summary_result.get("summary_text", title)
            except Exception as e:
                logger.error(f"Summary error: {e}")

            articles.append({
                "title": title,
                "summary": summary,
                "sentiment": sentiment,
                "published": published_dt.isoformat(),
                "link": link,
            })

        except Exception as e:
            logger.error(f"News entry error: {e}")
            continue

    return sorted(articles, key=lambda x: x["published"], reverse=True)
