
from typing import List, Dict, Tuple
import pandas as pd
from textblob import TextBlob

# каждый отзыв
Review = Dict[str, str]  # пример: {"text": "great!", "category": "movie"}

# результат анализа
AnalyzedReview = Dict[str, object]  # {"text": "...", "polarity": 0.8, "label": "positive"}


def load_reviews_from_csv(path: str) -> List[Review]:  # считывает отзывы
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось найти файл: {path}")

    if 'review_text' not in df.columns:
        raise ValueError("Не удалось найти колонку 'review_text'")

    # заменяем пропущенные значения на пустые строки и приводим все объекты к строкам
    df = df.fillna("")
    df = df.astype(str)

    # преобразуем в список словарей
    return df.to_dict(orient='records')


def predict_sentiment(text: str) -> Tuple[float, str]:  # анализирует тональность одного отзыва
    if not isinstance(text, str) or not text.strip():
        return 0.0, "neutral"

    # определяем polarity
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # от -1.0 до +1.0

    # в зависимости от polarity присваиваем label
    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return polarity, label


def analyze_reviews(reviews: List[Review]) -> List[AnalyzedReview]:  # применяет ко всем отзывам
    analyzed = []
    for review in reviews:
        # сохраняем исходный отзыв
        new_review = review.copy()
        # анализируем текст
        text = review.get("review_text", "")
        polarity, label = predict_sentiment(text)
        # добавляем результаты
        new_review["polarity"] = polarity
        new_review["sentiment_label"] = label
        analyzed.append(new_review)
    return analyzed


def compute_statistics(analyzed: List[AnalyzedReview]) -> Dict[str, int]:  # считает статистику
    pass


def export_results(analyzed: List[AnalyzedReview], output_dir: str) -> None:  # сохраняет результаты
    pass
