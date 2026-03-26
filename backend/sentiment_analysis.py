"""
News sentiment analysis module for stock predictions.
Uses TextBlob and newsapi for sentiment analysis.
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta
import requests
from textblob import TextBlob

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment from news articles."""

    def __init__(self, news_api_key: str = None, cache_hours: int = 24):
        """
        Initialize sentiment analyzer.

        Args:
            news_api_key: API key for newsapi.org
            cache_hours: Cache news articles for this many hours
        """
        self.news_api_key = news_api_key
        self.cache_hours = cache_hours
        self.news_api_url = "https://newsapi.org/v2/everything"

    def fetch_news(self, ticker: str, limit: int = 50) -> List[Dict]:
        """
        Fetch recent news for a stock ticker.

        Args:
            ticker: Stock ticker symbol
            limit: Number of articles to fetch

        Returns:
            List of news articles
        """
        try:
            if not self.news_api_key:
                logger.warning("News API key not configured. Returning empty results.")
                return []

            params = {
                "q": ticker,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": limit,
                "apiKey": self.news_api_key,
            }

            response = requests.get(self.news_api_url, params=params, timeout=10)
            response.raise_for_status()

            articles = response.json().get("articles", [])
            logger.info(f"Fetched {len(articles)} articles for {ticker}")
            return articles

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching news: {str(e)}")
            return []

    def analyze_sentiment(self, articles: List[Dict]) -> Dict:
        """
        Analyze sentiment of articles.

        Args:
            articles: List of article dictionaries

        Returns:
            Sentiment analysis results
        """
        if not articles:
            return self._neutral_response(0)

        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            text = f"{title} {description}".strip()

            if not text:
                continue

            # Analyze sentiment using TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1

            sentiments.append(polarity)

            if polarity > 0.1:
                positive_count += 1
            elif polarity < -0.1:
                negative_count += 1
            else:
                neutral_count += 1

        if not sentiments:
            return self._neutral_response(len(articles))

        # Calculate overall sentiment
        overall_sentiment = sum(sentiments) / len(sentiments)

        return {
            "sentiment_score": float(overall_sentiment),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "articles_analyzed": len(sentiments),
            "interpretation": self._interpret_sentiment(overall_sentiment),
        }

    def analyze_ticker_sentiment(self, ticker: str, limit: int = 50) -> Dict:
        """
        Fetch and analyze sentiment for a ticker in one call.

        Args:
            ticker: Stock ticker symbol
            limit: Number of articles to fetch

        Returns:
            Sentiment analysis results with article data
        """
        try:
            articles = self.fetch_news(ticker, limit)
            sentiment_result = self.analyze_sentiment(articles)
            sentiment_result["ticker"] = ticker
            sentiment_result["timestamp"] = datetime.utcnow().isoformat()
            return sentiment_result

        except Exception as e:
            logger.error(f"Error analyzing sentiment for {ticker}: {str(e)}")
            return self._neutral_response(0)

    @staticmethod
    def _neutral_response(article_count: int) -> Dict:
        """Return neutral sentiment response."""
        return {
            "sentiment_score": 0.0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": article_count,
            "articles_analyzed": article_count,
            "interpretation": "Neutral",
        }

    @staticmethod
    def _interpret_sentiment(score: float) -> str:
        """
        Interpret sentiment score.

        Args:
            score: Sentiment score from -1 to 1

        Returns:
            Sentiment interpretation
        """
        if score > 0.3:
            return "Very Positive"
        elif score > 0.1:
            return "Positive"
        elif score < -0.3:
            return "Very Negative"
        elif score < -0.1:
            return "Negative"
        else:
            return "Neutral"
