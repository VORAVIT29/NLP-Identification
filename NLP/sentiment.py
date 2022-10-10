from textblob import TextBlob

def sentiment(Text):
    # Create a textblob object
    blob_text = TextBlob(Text)
    # Print out its sentiment
    level_sentiment = blob_text.sentiment.polarity

    if level_sentiment >= -1.0 and level_sentiment < 0.0:
        return f"Negative {level_sentiment}"
    elif level_sentiment > 0.0:
        return f"Positive {level_sentiment}"
    return f"Neutral {level_sentiment}"


# print(sentiment("""You are so stupid"""))
