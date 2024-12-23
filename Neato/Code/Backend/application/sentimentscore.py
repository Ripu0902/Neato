# nltk.download('vader_lexicon')
import nltk
# nltk.download('punkt_tab')
# nltk.download('stopwords')

from nltk.sentiment import SentimentIntensityAnalyzer

import re

def analyze_sentiment(text, rating=None):
    """
    Analyze sentiment of review text using NLTK's VADER sentiment analyzer
    and combine it with numerical rating if provided.
    
    Args:
        text (str): Review text
        rating (float, optional): Numerical rating (1-5 scale)
    
    Returns:
        dict: Sentiment analysis results including scores and category
    """
    # Clean the text
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    
    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Get VADER sentiment scores
    sentiment_scores = sia.polarity_scores(text)
    
    # Calculate weighted score (0-100 scale)
    text_score = ((sentiment_scores['compound'] + 1) / 2) * 100
    
    # If rating is provided, combine it with text sentiment
    if rating is not None:
        # Convert rating to 0-100 scale
        rating_score = (rating / 5) * 100
        # Combine scores (60% weight to text, 40% to rating)
        final_score = (text_score * 0.6) + (rating_score * 0.4)
    else:
        final_score = text_score
    
    return round(final_score, 1)



# review = input()
# print(analyze_sentiment(review))